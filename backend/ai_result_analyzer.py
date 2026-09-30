import os
import json

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def load_results():

    with open("backend/test_results.json", "r") as file:
        results = json.load(file)

    return results


def analyze_results(results):

    prompt = """
You are an API quality assurance expert.

Analyze these real API test results.

Provide:

1. Overall test summary
2. Problems found
3. Failed or skipped tests
4. Possible reasons
5. Recommended actions

Important:
- Do not invent expected status codes.
- Use only the information present in the test results.
- Clearly distinguish between actual failures and skipped tests.
- Keep the explanation simple and clear.

Test results:

{}
""".format(results)

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


results = load_results()

analysis = analyze_results(results)

print()
print("AI QUALITY ANALYSIS")
print("===================")
print(analysis)