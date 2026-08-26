#this will be used to create an asynchronus context manager
from contextlib import asynccontextmanager

from fastapi import FastAPI
from project1.database import create_db_and_tables
from project1.routers import accounts #only include accounts router for my specifc testing

#defines the lifespan of the function
@asynccontextmanager
async def lifespan(app: FastAPI): #
	create_db_and_tables() #runs when the application starts, creating the table if it currently doesnt exist
	yield #code before yield will run during startup, code after yield will run during the shutdown. and fastapi runs the app while we are paused here at yiled

#creates our fastapi app and lets it know to use our lifespan function. without this fastapi wouldnt know to run the function upon startup
app = FastAPI(lifespan=lifespan)

#this adds all of the routes from accounts.py to our main fastapi app
app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])