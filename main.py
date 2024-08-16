from fastapi import FastAPI
from api.routers import codereview

app = FastAPI()

app.include_router(codereview.router, prefix="/api/v1/codereview")
