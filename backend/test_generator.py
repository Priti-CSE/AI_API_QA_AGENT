import requests


def get_api_spec():
    response = requests.get("http://127.0.0.1:8001/openapi.json")

    if response.status_code == 200:
        return response.json()

    return None


def generate_test_cases():
    api_spec = get_api_spec()

    if api_spec is None:
        print("Could not get API specification")
        return

    print("Generated Test Cases:")
    print()

    for path in api_spec["paths"]:
        for method in api_spec["paths"][path]:

            print("Test Case:")
            print("Method:", method.upper())
            print("Endpoint:", path)

            if method.lower() == "get":
                print("Test: Check whether the data is returned")

            elif method.lower() == "post":
                print("Test: Check whether a new user can be created")

            elif method.lower() == "put":
                print("Test: Check whether a user can be updated")

            elif method.lower() == "delete":
                print("Test: Check whether a user can be deleted")

            print("------------------------")


generate_test_cases()