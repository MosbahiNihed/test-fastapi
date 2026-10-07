from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    body = client.get("/").json()
    assert "hello-fastapi" in body["message"]
    assert "version" in body


def test_hello():
    assert client.get("/hello/Nihed").json() == {"message": "Hello, Nihed!"}


def test_info_has_hostname():
    body = client.get("/info").json()
    assert body["hostname"]
    assert body["app"] == "hello-fastapi"


def test_echo():
    r = client.post("/echo", json={"message": "hi"})
    assert r.json() == {"echo": "hi", "length": 2}
    assert client.post("/echo", json={"message": ""}).status_code == 422


def test_health():
    assert client.get("/healthz").status_code == 200
    assert client.get("/readyz").status_code == 200
