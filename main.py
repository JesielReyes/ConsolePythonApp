from fastapi import FastAPI

from routers.account_router import router as account_router


app = FastAPI(
    title="Banking API",
    version="1.0"
)


app.include_router(account_router)


@app.get("/")
def home():
    return {"message": "Bank API is running"}