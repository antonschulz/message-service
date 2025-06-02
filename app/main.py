from fastapi import FastAPI
from .database import engine, Base
from . import models, routes

app = FastAPI(
    title="Message Service",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(routes.router)

# create database tables on startup (if they don't already exist)
Base.metadata.create_all(bind=engine)
