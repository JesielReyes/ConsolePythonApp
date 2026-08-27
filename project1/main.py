from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables
from routers import accounts, transactions, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Banking API",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
app.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)


app.include_router(
    transactions.router,
    prefix="/transactions",
    tags=["transactions"]
)
