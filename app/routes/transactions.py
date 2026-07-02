from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.crud import get_transactions_by_user_id
from app.database.database import get_db
from app.database.models import UserProfiles
from app.schemas.transaction import TransactionListResponse
from app.auth import current_active_user

router = APIRouter(
    prefix="/api/v1/transactions",
    tags=["transactions"],
)


@router.get(
    "/",
    response_model=TransactionListResponse,
)
async def get_my_transactions(
    user: UserProfiles = Depends(current_active_user),
    db: AsyncSession = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: Optional[int] = Query(default=None, ge=1, le=500),
):
    # user id comes from the token, never the request — tenant isolation lives here.
    transactions = await get_transactions_by_user_id(db, user_id=user.id, skip=skip, limit=limit)
    return {"transactions": transactions}