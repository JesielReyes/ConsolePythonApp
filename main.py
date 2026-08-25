from fastapi import FastAPI

from routers.account_router import router as account_router
from routers.user_router import router as user_router


app = FastAPI(
    title="Banking API",
    version="1.0"
)


app.include_router(account_router)
app.include_router(user_router)


@app.get("/")
def home():
    return {"message": "Bank API is running"}