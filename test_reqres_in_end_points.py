import json

import requests
from jsonschema.validators import validate

from schemas import register, put_user


def test_email_at_user(user_id="2"):
    response = requests.get(
        url=f"https://reqres.in/api/users/{user_id}", headers={"x-api-key": "reqres-free-v1"})
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["data"]["email"] == 'janet.weaver@reqres.in'


def test_email_at_user_negative(user_id="3"):
    response = requests.get(
        url=f"https://reqres.in/api/users/{user_id}", headers={"x-api-key": "reqres-free-v1"})
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["data"]["first_name"] != 'Jannnnet'


def test_schema_validate_get_users(user_id="2"):
    response = requests.get(
        url=f"https://reqres.in/api/users/{user_id}", headers={"x-api-key": "reqres-free-v1"})
    response_json = response.json()
    assert response.status_code == 200
    with open("get_users.json") as file:
        validate(response_json, schema=json.loads(file.read()))


def test_register_user():
    payload = {"email": "eve.holt@reqres.in", "password": "pistol"}
    response = requests.post(
        url=f"https://reqres.in/api/register", headers={"x-api-key": "reqres-free-v1"}, data=payload)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["token"] != 0


def test_create_user_negative():
    payload = {"email": "eve.holt@ya.ru", "password": "pistol"}
    response = requests.post(
        url=f"https://reqres.in/api/register", headers={"x-api-key": "reqres-free-v1"}, data=payload)
    response_json = response.json()
    assert response.status_code == 400
    assert response_json["error"] == "Note: Only defined users succeed registration"


def test_schema_validate_register():
    payload = {"email": "eve.holt@reqres.in", "password": "pistol"}
    response = requests.post(
        url=f"https://reqres.in/api/register", headers={"x-api-key": "reqres-free-v1"}, data=payload)
    response_json = response.json()
    validate(response_json, schema=register)


def test_put_user(user_id="2"):
    payload = {"name": "morpheus", "job": "new job"}
    response = requests.put(
        url=f"https://reqres.in/api/users/{user_id}", headers={"x-api-key": "reqres-free-v1"}, data=payload)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["job"] == "new job"


def test_schema_validate_put_user(user_id="2"):
    payload = {"name": "morpheus", "job": "new job"}
    response = requests.put(
        url=f"https://reqres.in/api/users/{user_id}", headers={"x-api-key": "reqres-free-v1"}, data=payload)
    response_json = response.json()
    assert response.status_code == 200
    validate(response_json, schema=put_user)