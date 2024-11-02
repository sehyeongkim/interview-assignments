import pytest
from http.client import HTTPConnection
from unittest.mock import Mock, patch
from jwt.exceptions import PyJWTError

from core.fastapi.middlewares import authentication
from core.fastapi.middlewares.authentication import AuthBackend, CurrentUser

auth_backend = AuthBackend()


@pytest.mark.asyncio
@patch.object(authentication, "jwt")
async def test_auth_backend(jwt_mock):
    conn_mock = Mock(spec=HTTPConnection)
    conn_mock.headers = {"Authorization": "bearer authenticated"}
    jwt_mock.decode.return_value = {"user_id": 'uuid'}

    authenticated, user = await auth_backend.authenticate(conn=conn_mock)

    assert authenticated is True
    assert user == CurrentUser(id='uuid')

@pytest.mark.asyncio
async def test_auth_backend_empty_header():
    conn_mock = Mock(spec=HTTPConnection)
    conn_mock.headers = {}

    authenticated, user = await auth_backend.authenticate(conn=conn_mock)

    assert authenticated is False
    assert user.id is None

@pytest.mark.asyncio
async def test_auth_backend_invalid_header():
    conn_mock = Mock(spec=HTTPConnection)
    conn_mock.headers = {"Authorization": "Bearer123"}

    authenticated, user = await auth_backend.authenticate(conn=conn_mock)

    assert authenticated is False
    assert user.id is None

@pytest.mark.asyncio
async def test_auth_backend_not_startswith_bearer():
    conn_mock = Mock(spec=HTTPConnection)
    conn_mock.headers = {"Authorization": "token 1234"}

    authenticated, user = await auth_backend.authenticate(conn=conn_mock)

    assert authenticated is False
    assert user.id is None


@pytest.mark.asyncio
@patch.object(authentication, "jwt")
async def test_auth_backend_invalid_token(jwt_mock):
    conn_mock = Mock(spec=HTTPConnection)
    conn_mock.headers = {"Authorization": "Bearer"}
    jwt_mock.decode.side_effect = PyJWTError

    authenticated, user = await auth_backend.authenticate(conn=conn_mock)

    assert authenticated is False
    assert user.id is None


@pytest.mark.asyncio
async def test_auth_backend_empty_credentials():
    conn_mock = Mock(spec=HTTPConnection)
    conn_mock.headers = {"Authorization": "Bearer "}

    authenticated, user = await auth_backend.authenticate(conn=conn_mock)

    assert authenticated is False
    assert user.id is None
