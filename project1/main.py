from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from project1.routers import transactions
from routers import accounts, users

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exception: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "status_code": 422,
            "message": "Invalid request",
            "data": exception.errors()
        }
    )

app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])