import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv('/Users/qoala/Desktop/services/ai-service/.env')

class Settings(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    github_token: str = os.getenv("GITHUB_TOKEN")

settings = Settings()
