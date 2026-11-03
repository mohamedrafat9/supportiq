from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def test_health_check():
    response=client.get("/health")

    assert response.status_code==200
    assert response.json()=={"status":"ok"}

def test_create_ticket(client):
    response = client.post(
        "/tickets/",
        json={"title": "Test ticket"},
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Test ticket"
    assert data["status"] == "open"
    assert "id" in data

def test_read_ticket(client):
    create_response = client.post(
        "/tickets/",
        json={"title": "Read test ticket"},
    )

    ticket_id = create_response.json()["id"]

    response = client.get(f"/tickets/{ticket_id}")

    assert response.status_code == 200
    assert response.json()["id"] == ticket_id
    assert response.json()["title"] == "Read test ticket"
    assert response.json()["status"] == "open"

def test_read_nonexistent_ticket(client):
    response = client.get("/tickets/99999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}

def test_update_ticket_status(client):
    create_response = client.post(
        "/tickets/",
        json={"title": "Update test ticket"},
    )

    ticket_id = create_response.json()["id"]

    response = client.put(
        f"/tickets/{ticket_id}",
        json={"status": "in_progress"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == ticket_id
    assert response.json()["status"] == "in_progress"

def test_update_ticket_invalid_status(client):
    create_response = client.post(
        "/tickets/",
        json={"title": "Invalid status test"},
    )

    ticket_id = create_response.json()["id"]

    response = client.put(
        f"/tickets/{ticket_id}",
        json={"status": "pending"},
    )

    assert response.status_code == 422

def test_delete_ticket(client):
    create_response = client.post(
        "/tickets/",
        json={"title": "Delete test ticket"},
    )

    ticket_id = create_response.json()["id"]

    response = client.delete(f"/tickets/{ticket_id}")

    assert response.status_code == 204

    get_response = client.get(f"/tickets/{ticket_id}")

    assert get_response.status_code == 404

def test_delete_nonexistent_ticket(client):
    response = client.delete("/tickets/99999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "the ticket wasn't found"
    }


def test_read_all_tickets(client):
    client.post(
        "/tickets/",
        json={"title": "First ticket"},
    )

    client.post(
        "/tickets/",
        json={"title": "Second ticket"},
    )

    response = client.get("/tickets/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] == "First ticket"
    assert data[1]["title"] == "Second ticket"

def test_update_nonexistent_ticket(client):
    response = client.put(
        "/tickets/99999",
        json={"status": "in_progress"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}

def test_root(client):
    response=client.get("/")

    assert response.status_code==200
    assert response.json()=={"root":"hey this the root page "}

def test_cannot_reopen_closed_ticket(client):
    response = client.post(
        "/tickets/",
        json={"title": "Test ticket"},
    )
    ticket_id = response.json()["id"]

    client.put(
        f"/tickets/{ticket_id}",
        json={"status": "closed"},
    )

    response = client.put(
        f"/tickets/{ticket_id}",
        json={"status": "in_progress"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot reopen a closed ticket"