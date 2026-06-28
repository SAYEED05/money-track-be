from fastapi import APIRouter
from app.database.database import SessionLocal
from sqlalchemy import text
router = APIRouter(prefix="/api/v1/transactions", tags=["transactions"])

@router.get('/')
def read_transactions():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT * FROM transactions"))
        transactions = result.mappings().all()
        return {"transactions": [dict(row) for row in transactions]}
    finally:
        db.close()