import json

from src.api.models import User


def test_add_user(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"username": "luciano", "email": "luciano@test.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "luciano@test.io was added" in data["message"]


def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_invalid_json_keys(test_app, test_database):

    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"email": "luciano@test.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    client.post(
        "/users",
        data=json.dumps({"email": "luciano@test.io", "username": "luciano"}),
        content_type="application/json",
    )
    resp = client.post(
        "/users",
        data=json.dumps({"email": "luciano@test.io", "username": "luciano"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. That email already exists." in data["message"]


def test_single_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]


def test_single_user(test_app, test_database, add_user):
    user = add_user("luciano", "luciano@test.io")
    client = test_app.test_client()
    resp = client.get(f"/users/{user.id}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "luciano" in data["username"]
    assert "luciano@test.io" in data["email"]


def test_all_users(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    add_user("michael", "michael@test.io")
    add_user("luba", "luba@test.io")
    client = test_app.test_client()
    resp = client.get("/users")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert "michael" in data[0]["username"]
    assert "michael@test.io" in data[0]["email"]
    assert "luba" in data[1]["username"]
    assert "luba@test.io" in data[1]["email"]
