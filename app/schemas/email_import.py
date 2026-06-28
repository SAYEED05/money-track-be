from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ==========================================================
# Email Import Schemas
# ==========================================================

class EmailImportResponse(BaseModel):
    id: int
    user_id: int
    message_id: str
    sender: str
    subject: str
    raw_content: str
    received_at: datetime

    processed_at: Optional[datetime] = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Response for:
# GET /email-imports
# GET /email-imports/{user_id}

class EmailImportListResponse(BaseModel):
    email_imports: list[EmailImportResponse]