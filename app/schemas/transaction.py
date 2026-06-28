from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict

# ==========================================================
# Transaction Schemas
# ==========================================================

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: Decimal
    currency: str
    direction: str
    account_name: str
    transaction_date: datetime
    source: str

    counter_party: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    email_import_id: Optional[int] = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Response for:
# GET /transactions
# GET /transactions/{user_id}

class TransactionListResponse(BaseModel):
    transactions: list[TransactionResponse]