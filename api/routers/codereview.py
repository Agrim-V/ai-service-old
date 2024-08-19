from fastapi import APIRouter, HTTPException
from services.codereview import perform_code_review
import os
from dotenv import load_dotenv

load_dotenv('/Users/qoala/Desktop/services/ai-service/.env')

router = APIRouter()

@router.post("/review")
async def review_pull_request(owner: str, repo: str, pr_number: int):
    try:
        print(f"Received request with owner: {owner}, repo: {repo}, pr_number: {pr_number}")
        result = perform_code_review(owner, repo, pr_number)
        print(f"Code review result: {result}")
        return {"result": result}
    except Exception as e:
        print(f"Exception occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
