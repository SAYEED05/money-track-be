import os

from fastapi import Depends
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users.db import SQLAlchemyUserDatabase

from app.database.database import get_db
from app.database.models import UserProfiles

SECRET = os.getenv('SECRET_KEY')
if not SECRET or SECRET == 'change-me':
    raise RuntimeError('SECRET_KEY must be set to a real secret (not the change-me placeholder)')

ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '60')) * 60


async def get_user_db(session=Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, UserProfiles)


class UserManager(IntegerIDMixin, BaseUserManager[UserProfiles, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl='api/v1/auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=ACCESS_TOKEN_EXPIRE_SECONDS)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[UserProfiles, int](get_user_manager, [auth_backend])

# The choke point: use as `Depends(current_active_user)` in any protected route.
current_active_user = fastapi_users.current_user(active=True)
