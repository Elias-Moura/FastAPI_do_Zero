from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse

from database import get_session
from exceptions.UserAlreadyExists import UserAlreadyExists
from exceptions.UserNotFoundException import UserNotFoundException
from fast_zero.models import User

# from database import get_session
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()


@app.get('/', status_code=200, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/html', status_code=200, response_class=HTMLResponse)
def hw_html():
    return '<h1>Hello World!</h1>'


@app.post('/users', status_code=201, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.username == user.username)
    )

    if db_user:
        raise UserAlreadyExists()

    db_user = User(
        username=user.username, email=user.email, password=user.password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users', status_code=200, response_model=UserList)
def get_users(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@app.get('/users/{user_id}', status_code=200, response_model=UserPublic)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.id == user_id))
    if not user:
        raise UserNotFoundException()
    return user


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise UserNotFoundException()

    db_user.username = user.username
    db_user.password = user.password
    db_user.email = user.email

    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise UserNotFoundException()

    session.delete(db_user)
    session.commit()
    return {'message': 'User deleted.'}
