from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.models import Transactions


async def get_all_transactions(db: AsyncSession, skip: int = 0, limit: int | None = None):
    stmt = select(Transactions).order_by(Transactions.transaction_date.desc()).offset(skip)
    if limit is not None:
        stmt = stmt.limit(limit)

    result = await db.execute(stmt)
    return result.scalars().all()


async def get_transactions_by_user_id(
    db: AsyncSession,
    user_id: int,
    skip: int = 0,
    limit: int | None = None,
):
    stmt = (
        select(Transactions)
        .where(Transactions.user_id == user_id)
        .order_by(Transactions.transaction_date.desc())
        .offset(skip)
    )
    if limit is not None:
        stmt = stmt.limit(limit)

    result = await db.execute(stmt)
    return result.scalars().all()
