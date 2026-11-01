VALID = {
    "caller_name": "Test Caller",
    "caller_phone": "9000000001",
    "emergency_type": "accident",
    "severity": "high",
    "location_address": "Test Street 1, Demo City",
}


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["database"] == "connected"


def test_create_and_fetch(client):
    r = client.post("/api/emergencies", json=VALID)
    assert r.status_code == 201
    new_id = r.json()["id"]
    assert r.json()["status"] == "pending"

    assert client.get("/api/emergencies").json()["total"] == 1
    detail = client.get(f"/api/emergencies/{new_id}").json()
    assert detail["status_history"][0]["new_status"] == "pending"


def test_validation_errors(client):
    bad = dict(VALID, caller_phone="abc", emergency_type="unknown")
    assert client.post("/api/emergencies", json=bad).status_code == 422
    assert client.post("/api/emergencies", json=dict(VALID, latitude=10.0)).status_code == 422
    assert client.post("/api/emergencies", json=dict(VALID, patient_age=200)).status_code == 422


def test_not_found(client):
    assert client.get("/api/emergencies/999").status_code == 404
    r = client.patch("/api/emergencies/999/status", json={"status": "assigned"})
    assert r.status_code == 404


def test_status_flow_and_invalid_jump(client):
    new_id = client.post("/api/emergencies", json=VALID).json()["id"]
    url = f"/api/emergencies/{new_id}/status"

    assert client.patch(url, json={"status": "completed"}).status_code == 409
    assert client.patch(url, json={"status": "assigned"}).status_code == 200

    detail = client.get(f"/api/emergencies/{new_id}").json()
    assert detail["status"] == "assigned"
    assert len(detail["status_history"]) == 2

    client.patch(url, json={"status": "cancelled"})
    assert client.patch(url, json={"status": "assigned"}).status_code == 409  # closed


def test_filter_and_summary(client):
    client.post("/api/emergencies", json=VALID)
    client.post("/api/emergencies", json=dict(VALID, severity="critical"))
    assert client.get("/api/emergencies?severity=critical").json()["total"] == 1
    summary = client.get("/api/dashboard/summary").json()
    assert summary["total_emergencies"] == 2
    assert summary["by_severity"]["high"] == 1
