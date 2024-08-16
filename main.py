from fastapi import FastAPI
from app.api.v1.endpoints import codereview

app = FastAPI()

app.include_router(codereview.router, prefix="/api/v1/codereview")
