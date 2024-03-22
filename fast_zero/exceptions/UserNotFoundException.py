from http import HTTPStatus
from http.client import HTTPException


class UserNotFoundException(HTTPException):
    def __init__(self):
        self.status_code = HTTPStatus.NOT_FOUND.value
        self.detail = 'User not found.'
        self.args = ({'status_code': self.status_code, 'detail': self.detail},)
