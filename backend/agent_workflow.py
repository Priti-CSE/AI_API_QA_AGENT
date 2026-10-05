import sys
import time
sys.stdout.reconfigure(encoding="utf-8")

import os
import json
import requests

from typing import TypedDict
from redis_cache import save_results

from dotenv import load_dotenv
from groq import Groq

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from langgraph.graph import StateGraph, START, END


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BASE_URL = "http://127.0.0.1:8001"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

class QAState(TypedDict):
    api_spec: dict
    test_cases: dict
    test_results: list
    report: str


def analyze_api(state: QAState):

    print("Analyzing API...")

    response = requests.get(
        BASE_URL + "/openapi.json"
    )

    api_spec = response.json()

    print("API analysis completed.")

    return {
        "api_spec": api_spec
    }

def generate_tests(state: QAState):

    print("Generating AI test cases...")

    api_spec = state["api_spec"]

    prompt = """
You are an API testing expert.

Analyze this OpenAPI specification.

Generate API test cases.

For each test case provide:

- name
- method
- endpoint
- body
- expected_status

Include functional, negative and validation tests.

Return ONLY valid JSON.

Use this structure:

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

    result = json.loads(
        response.choices[0].message.content
    )

    print("AI test cases generated.")

    return {
        "test_cases": result
    }

def execute_tests(state: QAState):

    print("Executing AI test cases...")

    test_cases = state["test_cases"]["test_cases"]

    results = []

    for test in test_cases:

        method = test["method"]
        endpoint = test["endpoint"]
        body = test.get("body")

        if "expected_status" not in test:

            results.append({
                "name": test["name"],
                "method": method,
                "endpoint": endpoint,
                "expected": None,
                "actual": None,
                "result": "SKIPPED"
            })

            continue

        expected_status = test["expected_status"]

        url = BASE_URL + endpoint

        start_time = time.perf_counter()

        response = requests.request(
            method=method,
            url=url,
            json=body
        )

        end_time = time.perf_counter()

        response_time = round(
            (end_time - start_time) * 1000,
            2
        )

        actual_status = response.status_code

        if actual_status == expected_status:
            result = "PASS"
        else:
            result = "FAIL"

        results.append({
            "name": test["name"],
            "method": method,
            "endpoint": endpoint,
            "expected": expected_status,
            "actual": actual_status,
            "response_time": response_time,
            "result": result
        })
        print("Test execution completed.")

    save_results(results)

    with open("backend/test_results.json", "w") as file:
            json.dump(results, file, indent=4)

    return {
        "test_results": results
    }

def analyze_results(state: QAState):

    print("Analyzing test results with AI...")

    results = state["test_results"]

    query = "API testing status codes negative testing failures"

    rag_results = vector_store.similarity_search(
        query,
        k=2
    )

    knowledge = ""

    for result in rag_results:
        knowledge = knowledge + result.page_content + "\n"

    prompt = """
You are an API quality assurance expert.

Use this API testing knowledge:

{}

Analyze these actual API test results:

{}

Give the following information:

1. Overall test summary
2. Number of passed tests
3. Number of failed tests
4. Number of skipped tests
5. Problems found
6. Possible reasons for failures
7. Recommended actions

Important:
- Use only the information provided in the test results.
- Do not invent test results.
- Clearly distinguish PASS, FAIL and SKIPPED.
- Keep the explanation simple.
""".format(knowledge, results)

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    report = response.choices[0].message.content

    print("AI analysis completed.")

    total = len(results)
    passed = 0
    failed = 0
    skipped = 0

    for result in results:
        if result["result"] == "PASS":
            passed += 1
        elif result["result"] == "FAIL":
            failed += 1
        elif result["result"] == "SKIPPED":
            skipped += 1

    qa_report = {
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "ai_analysis": report
    }

    with open("backend/qa_report.json", "w") as file:
        json.dump(qa_report, file, indent=4)

    print("QA report created successfully.")

    return {
        "report": report
    }
builder = StateGraph(QAState)

builder.add_node("analyze_api", analyze_api)
builder.add_node("generate_tests", generate_tests)
builder.add_node("execute_tests", execute_tests)
builder.add_node("analyze_results", analyze_results)
builder.add_edge(START, "analyze_api")
builder.add_edge("analyze_api", "generate_tests")
builder.add_edge("generate_tests", "execute_tests")
builder.add_edge("execute_tests", "analyze_results")
builder.add_edge("analyze_results", END)
workflow = builder.compile()


result = workflow.invoke({
    "api_spec": {},
    "test_cases": {},
    "test_results": [],
    "report": ""
})

print()
print("LANGGRAPH WORKFLOW RESULT")
print("=========================")
print("Number of test cases:",
      len(result["test_cases"]["test_cases"]))
print("Number of test results:",
      len(result["test_results"]))
print()
print("AI QUALITY REPORT")
print("=================")
print(result["report"])