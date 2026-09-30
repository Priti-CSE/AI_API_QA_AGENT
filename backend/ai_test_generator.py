import os
import requests
import json

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_api_spec():
    response = requests.get(
        "http://127.0.0.1:8001/openapi.json"
    )

    if response.status_code == 200:
        return response.json()

    return None


def generate_ai_tests(api_spec):

    prompt = """
You are an API testing expert.

Analyze the following OpenAPI specification.

Generate API test cases.

For each test case provide:

- name
- method
- endpoint
- body
- expected_status

Include:
1. Functional tests
2. Negative tests
3. Validation tests
4. Boundary tests

Return ONLY valid JSON.

The JSON must follow this structure:

{{
    "test_cases": [
        {{
            "name": "Get all users",
            "method": "GET",
            "endpoint": "/users",
            "body": null,
            "expected_status": 200
        }}
    ]
}}

OpenAPI specification:

{}
""".format(api_spec)

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content


api_spec = get_api_spec()

if api_spec is not None:

    result = generate_ai_tests(api_spec)

    test_data = json.loads(result)

    with open("backend/ai_generated_tests.json", "w") as file:
        json.dump(test_data, file, indent=4)

    print("AI test cases generated successfully.")
    print("Saved to backend/ai_generated_tests.json")

else:

    print("Could not get API specification")