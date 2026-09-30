import os
import requests

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

Generate API test cases for the available endpoints.

Include:
1. Functional test cases
2. Negative test cases
3. Validation test cases
4. Boundary test cases

For each test case, provide:
- Test name
- HTTP method
- Endpoint
- Request data if required
- Expected HTTP status code

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
        ]
    )

    return response.choices[0].message.content

api_spec = get_api_spec()

if api_spec is not None:
    result = generate_ai_tests(api_spec)
    print(result)
else:
    print("Could not get API specification")