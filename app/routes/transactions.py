from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.crud import get_all_transactions, get_transactions_by_user_id
from app.database.database import get_db
from app.schemas.transaction import TransactionListResponse

router = APIRouter(
    prefix="/api/v1/transactions",
    tags=["transactions"],
)

@router.get(
    "/",
    response_model=TransactionListResponse,
)
def get_transactions(
    db: Session = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: Optional[int] = Query(default=None, ge=1, le=500),
):
    transactions = get_all_transactions(db, skip=skip, limit=limit)
    return {"transactions": transactions}


@router.get(
    "/user/{user_id}",
    response_model=TransactionListResponse,
)
def get_transactions_for_user(
    user_id: int,
    db: Session = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: Optional[int] = Query(default=None, ge=1, le=500),
):
    transactions = get_transactions_by_user_id(db, user_id=user_id, skip=skip, limit=limit)
    return {"transactions": transactions}