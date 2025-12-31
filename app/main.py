from fastapi import FastAPI
from app.api.query import router

app = FastAPI(title="NL2SQL Compiler")
app.include_router(router)
