from core.exceptions.base import CustomException


class DuplicatedUserEmail(CustomException):
    code = 400
    error_code = 'USER_DUPLICATE_EMAIL'
    message = 'duplicate email'


class DecodeTokenException(CustomException):
    code = 400
    error_code = "TOKEN_DECODE_ERROR"
    message = "token decode error"


class ExpiredTokenException(CustomException):
    code = 400
    error_code = "TOKEN_EXPIRE_TOKEN"
    message = "expired token"


class UserNotFoundException(CustomException):
    code = 404
    error_code = 'USER_NOT_FOUND'
    messsage = 'user not found'


class PasswordDoesNotMatchException(CustomException):
    code = 400
    error_code = 'PASSWORD_DOES_NOT_MATCH'
    message = 'user not found'

class NothingToUpdateUserInfoException(CustomException):
    code = 400
    error_code = 'NOTHING_TO_UPDATE'
    message = 'update info does not exist'
