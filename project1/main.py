from fastapi import FastAPI
from project1.routers import transactions
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routers import accounts, users
from contextlib import asynccontextmanager
from project1.database import create_db_and_tables

#defines the lifespan of the function
@asynccontextmanager
async def lifespan(app: FastAPI): #
	create_db_and_tables() #runs when the application starts, creating the table if it currently doesnt exist
	yield #code before yield will run during startup, code after yield will run during the shutdown. and fastapi runs the app while we are paused here at yiled

#creates our fastapi app and lets it know to use our lifespan function. without this fastapi wouldnt know to run the function upon startup
app = FastAPI(lifespan=lifespan)

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