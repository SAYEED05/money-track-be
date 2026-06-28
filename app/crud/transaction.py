from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.models import Transactions


def get_all_transactions(db: Session, skip: int = 0, limit: int | None = None):
    stmt = select(Transactions).order_by(Transactions.transaction_date.desc()).offset(skip)
    if limit is not None:
        stmt = stmt.limit(limit)

    return db.execute(stmt).scalars().all()
