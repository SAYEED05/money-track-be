from typing import Optional

from fastapi_users import schemas
from pydantic import Field


# ==========================================================
# User Schemas (fastapi-users) — `username` is added so register/read carry it.
# ==========================================================

class UserRead(schemas.BaseUser[int]):
    username: str
    # Required by BaseUser, but kept out of API responses. Flip in the DB or a separate admin API.
    is_superuser: bool = Field(default=False, exclude=True)
    is_verified: bool = Field(default=False, exclude=True)


class UserCreate(schemas.BaseUserCreate):
    username: str


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None