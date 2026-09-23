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


test_get_users()
test_get_user()
test_invalid_user()