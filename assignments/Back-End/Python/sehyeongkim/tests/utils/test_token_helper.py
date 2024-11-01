import jwt
import pytest

from core.config import config
from core.utils.token_helper import TokenHelper
from core.exceptions.user import DecodeTokenException, ExpiredTokenException

EXPIRED_USER_ID = '244c9b75-140c-4f5f-b7c1-81e94c38f90f'
EXPIRED_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMjQ0YzliNzUtMTQwYy00ZjVmLWI3YzEtODFlOTRjMzhmOTBmIiwiZXhwIjoxNzMwMjg5Nzg3fQ.A6uxjTRoyqR5MjFyRYpMiSHSVFSc9KGLjqcGAMDokmQ'

@pytest.mark.asyncio
async def test_encode():
    payload = {'user_id': 1}
    token = TokenHelper.encode(payload=payload)
    decoded_token = jwt.decode(
        token, config.JWT_SECRET_KEY, config.JWT_ALGORITHM
    )
    assert decoded_token['user_id'] == 1


@pytest.mark.asyncio
async def test_decode():
    token = jwt.encode({'user_id': 1}, config.JWT_SECRET_KEY, config.JWT_ALGORITHM)
    result = TokenHelper.decode(token=token)
    assert result == {'user_id': 1}


@pytest.mark.asyncio
async def test_decode_expired_decode_error():
    token = 'invalid'
    with pytest.raises(DecodeTokenException):
        TokenHelper.decode(token=token)


@pytest.mark.asyncio
async def test_decode_expired_signature_error():
    token = EXPIRED_TOKEN
    with pytest.raises(ExpiredTokenException):
        TokenHelper.decode(token=token)


@pytest.mark.asyncio
async def test_decode_expired_token():
    token = EXPIRED_TOKEN
    result = TokenHelper.decode_expired_token(token=token)
    assert result['user_id'] == EXPIRED_USER_ID


@pytest.mark.asyncio
async def test_decode_expired_token_decode_error():
    token = 'invalid'
    with pytest.raises(DecodeTokenException):
        TokenHelper.decode_expired_token(token=token)
