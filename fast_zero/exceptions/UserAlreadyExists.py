from http import HTTPStatus
from http.client import HTTPException


class UserAlreadyExists(HTTPException):
    def __init__(self):
        self.status_code = HTTPStatus.BAD_REQUEST.value
        self.detail = 'Username already registered.'
        self.args = ({'status_code': self.status_code, 'detail': self.detail},)
        # super().__init__(status_code=self.status_code, detail=self.detail)
