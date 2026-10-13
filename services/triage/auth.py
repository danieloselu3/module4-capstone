"""JWT auth (Week 6 auth.py, adapted): bcrypt users, /token, and the current_user doorman.

JWT_SECRET comes from the environment. With APP_ENV=production a missing secret refuses
to boot; otherwise a dev-only default is used and a warning is logged (Week 6 behaviour).
"""
import logging
import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, Field

from services.triage.security.rbac import OPS, PARTNER

log = logging.getLogger('auth')
ALGORITHM = 'HS256'
ISSUER = 'afyaplus-health-ops'
TOKEN_MINUTES = 30

JWT_SECRET = os.getenv('JWT_SECRET')
if not JWT_SECRET:
    if os.getenv('APP_ENV') == 'production':
        raise RuntimeError('JWT_SECRET is not set. Inject it at runtime; never commit it.')
    log.warning('JWT_SECRET not set: using the dev-only default (never in production)')
    JWT_SECRET = 'dev-only-secret-never-use-in-production-0000'

# bcrypt hashes only (copied from afyaplus-week9). Demo credentials are in docs/user_guide.md.
USERS = {
    'mercy': {'password_hash': '$2b$12$Ux5hVLI7NaH7kfRIcYjBUujTgR8OaKHMtBFcaTLUacoC0sZYddUwC', 'role': OPS},
    'guest': {'password_hash': '$2b$12$zaNC1fbtkITkh2bx5ns4eejT0/EDGWmmRxAAcZMc2Aa7rCn5BNnb2', 'role': PARTNER},
}
_DUMMY_HASH = b'$2b$12$S4Abn8hk37yF.898FmdtUeXK3iyOibuHSv8I/QjGCF12xP4jsRpuO'
_bearer = HTTPBearer(auto_error=False)


def check_password(username: str, password: str) -> bool:
    user = USERS.get(username)
    stored = user['password_hash'].encode() if user else _DUMMY_HASH
    return bcrypt.checkpw(password.encode(), stored) and user is not None


def create_token(username: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {'sub': username, 'role': USERS[username]['role'], 'iss': ISSUER,
               'iat': now, 'exp': now + timedelta(minutes=TOKEN_MINUTES)}
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)


def _unauthorized(detail: str) -> HTTPException:
    return HTTPException(status_code=401, detail=detail, headers={'WWW-Authenticate': 'Bearer'})


def current_user(creds: HTTPAuthorizationCredentials | None = Depends(_bearer)) -> dict:
    """401 unless the request carries a valid, unexpired bearer token."""
    if creds is None:
        raise _unauthorized("Not authenticated. POST /token, then send 'Authorization: Bearer <token>'.")
    try:
        return jwt.decode(creds.credentials, JWT_SECRET, algorithms=[ALGORITHM], issuer=ISSUER,
                          options={'require': ['exp', 'sub', 'role']})
    except jwt.ExpiredSignatureError:
        raise _unauthorized('Token expired. Log in again at /token.')
    except jwt.InvalidTokenError:
        raise _unauthorized('Invalid token.')


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    username: str = Field(min_length=3, max_length=32, pattern=r'^[a-z0-9_]+$')
    password: str = Field(min_length=8, max_length=128)


auth_router = APIRouter(tags=['auth'])


@auth_router.post('/token')
def login(body: LoginRequest):
    if not check_password(body.username, body.password):
        raise _unauthorized('Wrong username or password.')
    return {'access_token': create_token(body.username), 'token_type': 'bearer',
            'expires_in': TOKEN_MINUTES * 60}
