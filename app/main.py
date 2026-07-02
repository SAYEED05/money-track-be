from fastapi import FastAPI

from app.routes.transactions import router as transactions_router
from app.routes.user import router as user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(transactions_router)
