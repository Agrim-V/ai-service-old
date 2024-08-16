from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_review_pull_request():
    response = client.post("/api/v1/codereview/review", json={"owner": "owner_name", "repo": "repo_name", "pr_number": 1})
    assert response.status_code == 200
    assert "result" in response.json()
