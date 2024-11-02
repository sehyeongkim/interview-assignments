from core.exceptions.base import CustomException


class PostNotFoundException(CustomException):
    code = 404
    error_code = 'POST_NOT_FOUND'
    message = 'post not found'
