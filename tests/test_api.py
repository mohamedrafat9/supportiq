from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def test_health_check():
    response=client.get("/health")

    assert response.status_code==204
    assert response.json()=={"status":"okk"}