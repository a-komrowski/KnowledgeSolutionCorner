def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200

def test_home(client):
    r = client.get("/")
    assert r.status_code == 200
