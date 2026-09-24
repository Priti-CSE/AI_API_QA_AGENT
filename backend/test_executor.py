from urllib import response

import requests


def test_get_users():
    response = requests.get("http://127.0.0.1:8001/users")

    print("Test: GET /users")
    print("Expected Status: 200")
    print("Actual Status:", response.status_code)

    if response.status_code == 200:
        print("Result: PASS")
    else:
        print("Result: FAIL")

    print("------------------------")


def test_get_user():
    response = requests.get("http://127.0.0.1:8001/users/1")

    print("Test: GET /users/1")
    print("Expected Status: 200")
    print("Actual Status:", response.status_code)

    if response.status_code == 200:
        print("Result: PASS")
    else:
        print("Result: FAIL")

    print("------------------------")


def test_invalid_user():
    response = requests.get("http://127.0.0.1:8001/users/999")

    print("Test: GET /users/999")
    print("Expected Status: 404")
    print("Actual Status:", response.status_code)

    if response.status_code == 404:
        print("Result: PASS")
    else:
        print("Result: FAIL")

    print("------------------------")

def test_create_user():
    data = {
        "name": "Test User",
        "email": "test@example.com"
    }

    response = requests.post(
        "http://127.0.0.1:8001/users",
        json=data
    )

    print("Test: POST /users")
    print("Expected Status: 200")
    print("Actual Status:", response.status_code)

    if response.status_code == 200:
        print("Result: PASS")
    else:
        print("Result: FAIL")

    print("------------------------")

def test_create_user_missing_email():
    data = {
        "name": "Test User"
    }

    response = requests.post(
        "http://127.0.0.1:8001/users",
        json=data
    )

    print("Test: POST /users - Missing Email")
    print("Expected Status: 422")
    print("Actual Status:", response.status_code)

    if response.status_code == 422:
        print("Result: PASS")
    else:
        print("Result: FAIL")

    print("------------------------")

def test_update_user():
    data = {
        "name": "Updated User",
        "email": "updated@example.com"
    }

    response = requests.put(
        "http://127.0.0.1:8001/users/1",
        json=data
    )

    print("Test: PUT /users/1")
    print("Expected Status: 200")
    print("Actual Status:", response.status_code)

    if response.status_code == 200:
        print("Result: PASS")
    else:
        print("Result: FAIL")

    print("------------------------")

def test_delete_user():
    response = requests.delete(
        "http://127.0.0.1:8001/users/2"
    )

    print("Test: DELETE /users/2")
    print("Expected Status: 200")
    print("Actual Status:", response.status_code)

    if response.status_code == 200:
        print("Result: PASS")
    else:
        print("Result: FAIL")

    print("------------------------")

def test_delete_invalid_user():
    response = requests.delete(
        "http://127.0.0.1:8001/users/999"
    )

    print("Test: DELETE /users/999")
    print("Expected Status: 404")
    print("Actual Status:", response.status_code)

    if response.status_code == 404:
        print("Result: PASS")
    else:
        print("Result: FAIL")

    print("------------------------")

test_get_users()
test_get_user()
test_invalid_user()
test_create_user()
test_create_user_missing_email()
test_update_user()
test_delete_user()
test_delete_invalid_user()