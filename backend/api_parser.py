import requests


def get_api_spec():
    response = requests.get("http://127.0.0.1:8001/openapi.json")

    if response.status_code == 200:
        return response.json()

    return None


def analyze_api():
    api_spec = get_api_spec()

    if api_spec is None:
        print("Could not get API specification")
        return

    print("API Name:", api_spec["info"]["title"])
    print("Endpoints found:")

    for path in api_spec["paths"]:
        print("Endpoint:", path)

    for method in api_spec["paths"][path]:
        print("Method:", method.upper())

    print()


analyze_api()