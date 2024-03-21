from fastapi import FastAPI, HTTPException
from starlette.responses import HTMLResponse

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()


class UserRepository:
    def __init__(self):
        self.data_base = []

    def insert(self, user: UserSchema):
        user_with_id = UserDB(**user.model_dump(), id=len(self.data_base) + 1)
        self.data_base.append(user_with_id)
        return user_with_id

    def get_all(self):
        return self.data_base

    def __not_found(self, user_id: int) -> None:
        if user_id > len(self.data_base) or user_id < 1:
            raise HTTPException(status_code=404, detail='User not found.')

    def get_by_id(self, user_id: int) -> UserDB:
        self.__not_found(user_id)
        return self.data_base[user_id - 1]

    def update(self, user_id: int, user: UserSchema):
        self.__not_found(user_id)

        user_with_id = UserDB(**user.model_dump(), id=user_id)
        # O -1 é para ustar o indice da lista (na lista começamos a contar com 0)
        # e na nossa aplicação começamos a contar com 1
        self.data_base[user_id - 1] = user_with_id

        return user_with_id

    def delete(self, user_id: int):
        self.__not_found(user_id)

        del self.data_base[user_id - 1]


user_repository = UserRepository()


@app.get('/', status_code=200, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/html', status_code=200, response_class=HTMLResponse)
def hw_html():
    return '<h1>Hello World!</h1>'


@app.post('/users', status_code=201, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = user_repository.insert(user)
    return user_with_id


@app.get('/users', status_code=200, response_model=UserList)
def get_users():
    return {'users': user_repository.get_all()}


@app.get('/users/{user_id}', status_code=200, response_model=UserPublic)
def get_user(user_id: int):
    return user_repository.get_by_id(user_id)


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    user_with_id = user_repository.update(user_id, user)
    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    user_repository.delete(user_id)
    return {'message': 'User deleted.'}
