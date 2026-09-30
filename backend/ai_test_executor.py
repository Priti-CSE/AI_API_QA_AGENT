import json
import requests


BASE_URL = "http://127.0.0.1:8001"


def load_test_cases():

    with open("backend/ai_generated_tests.json", "r") as file:
        data = json.load(file)

    return data["test_cases"]


def run_test(test):

    method = test["method"]
    endpoint = test["endpoint"]
    body = test["body"]

    if "expected_status" not in test:
        print("--------------------------------")
        print("Test:", test["name"])
        print("Result: SKIPPED")
        print("Reason: Expected status code is missing")

        return {
            "name": test["name"],
            "method": method,
            "endpoint": endpoint,
            "expected": None,
            "actual": None,
            "result": "SKIPPED"
        }

    expected_status = test["expected_status"]

    url = BASE_URL + endpoint

    response = requests.request(
        method=method,
        url=url,
        json=body
    )

    actual_status = response.status_code

    if actual_status == expected_status:
        result = "PASS"
    else:
        result = "FAIL"

    print("--------------------------------")
    print("Test:", test["name"])
    print("Method:", method)
    print("Endpoint:", endpoint)
    print("Expected:", expected_status)
    print("Actual:", actual_status)
    print("Result:", result)

    return {
        "name": test["name"],
        "method": method,
        "endpoint": endpoint,
        "expected": expected_status,
        "actual": actual_status,
        "result": result
    }


test_cases = load_test_cases()

print("AI GENERATED API TESTS")
print("======================")

results = []

for test in test_cases:

    test_result = run_test(test)

    results.append(test_result)


with open("backend/test_results.json", "w") as file:
    json.dump(results, file, indent=4)


passed = 0
failed = 0
skipped = 0

for result in results:

    if result["result"] == "PASS":
        passed = passed + 1

    elif result["result"] == "FAIL":
        failed = failed + 1

    else:
        skipped = skipped + 1


print()
print("======================")
print("TEST SUMMARY")
print("======================")
print("Total:", len(results))
print("Passed:", passed)
print("Failed:", failed)
print("Skipped:", skipped)
print()
print("Results saved to backend/test_results.json")