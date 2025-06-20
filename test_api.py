import requests
import pytest
from jsonschema import validate

API = "reqres-free-v1"
HEADER = {
    "x-api-key": "reqres-free-v1"
}
schema = {
    "type": "object",
    "properties": {
        "page": {"type": "number"},
        "data": {"type": "array"}
    },
    "required": ["data"]
}

# GET запросы
def test_get_users():
    response = requests.get("https://reqres.in/api/users?page=2", headers=HEADER)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data

def test_get_users_schema():
    response = requests.get("https://reqres.in/api/users?page=2", headers=HEADER)
    validate(instance=response.json(), schema=schema)

def test_not_found():
    response = requests.get("https://reqres.in/api/users/999", headers=HEADER)
    assert response.status_code == 404

# POST запросы
def test_create_user():
    payload = {"name": "Alice", "job": "Engineer"}
    response = requests.post("https://reqres.in/api/users", json=payload, headers=HEADER)
    assert response.status_code == 201
    assert response.json().get("id") is not None

@pytest.mark.parametrize("name, job", [("Bob", "QA"), ("Eve", "DevOps")])
def test_create_user_params(name, job):
    response = requests.post("https://reqres.in/api/users", json={"name": name, "job": job}, headers=HEADER)
    assert response.status_code == 201

def test_invalid_login():
    response = requests.post("https://reqres.in/api/login", json={"email": "test@test"}, headers=HEADER)
    assert response.status_code == 400
    assert "error" in response.json()

# PUT запрос
def test_update_user():
    payload = {"name": "Alice", "job": "Senior Engineer"}
    response = requests.put("https://reqres.in/api/users/2", json=payload, headers=HEADER)
    assert response.status_code == 200
    assert response.json()["job"] == "Senior Engineer"

# DELETE запрос
def test_delete_user():
    response = requests.delete("https://reqres.in/api/users/2", headers=HEADER)
    assert response.status_code == 204
