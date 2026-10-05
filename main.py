from fastapi import FastAPI
from fastapi.responses import FileResponse
import json
import subprocess
import sys
import os
from datetime import datetime

app = FastAPI()


HISTORY_FILE = "backend/run_history.json"


def load_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    except:
        return []


def save_history(history):

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


@app.get("/")
def home():

    return FileResponse("dashboard/index.html")


@app.get("/results")
def get_results():

    with open("backend/test_results.json", "r") as file:
        results = json.load(file)

    formatted_results = []

    for result in results:

        formatted_results.append({
            "name": result.get("name", ""),
            "endpoint": result.get("endpoint", ""),
            "method": result.get("method", ""),
            "expected": result.get("expected"),
            "status_code": result.get("actual"),
            "response_time": result.get("response_time"),
            "passed": result.get("result") == "PASS",
            "result": result.get("result", ""),
            "error": ""
        })

    return formatted_results


@app.get("/analysis")
def get_analysis():

    try:

        with open("backend/qa_report.json", "r") as file:
            report = json.load(file)

    except:

        return {
            "available": False,
            "overall": "AI analysis is not available yet.",
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "pass_rate": 0,
            "issues": [],
            "ai_analysis": ""
        }

    try:

        with open("backend/test_results.json", "r") as file:
            results = json.load(file)

    except:

        results = []

    total = report.get("total_tests", len(results))
    passed = report.get("passed", 0)
    failed = report.get("failed", 0)
    skipped = report.get("skipped", 0)

    if total > 0:
        pass_rate = round((passed / total) * 100)
    else:
        pass_rate = 0

    issues = []

    for result in results:

        if result.get("result") == "FAIL":

            issues.append({
                "test": result.get("name", ""),
                "method": result.get("method", ""),
                "endpoint": result.get("endpoint", ""),
                "expected": result.get("expected"),
                "actual": result.get("actual")
            })

    if failed == 0:

        overall = (
            "All {} API tests passed successfully."
            .format(total)
        )

    else:

        overall = (
            "{} of {} tests passed and {} test(s) failed."
            .format(passed, total, failed)
        )

    return {
        "available": True,
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "pass_rate": pass_rate,
        "overall": overall,
        "issues": issues,
        "ai_analysis": report.get(
            "ai_analysis",
            "No AI analysis available."
        )
    }


@app.get("/history")
def get_history():

    history = load_history()

    return {
        "runs": history
    }


@app.get("/regressions")
def get_regressions():

    history = load_history()

    if len(history) < 2:
        return {
            "current_run": history[-1].get("run_number") if len(history) == 1 else None,
            "previous_run": None,
            "regressions": [],
            "fixed": [],
            "still_failing": []
        }

    previous = history[-2]
    latest = history[-1]

    previous_results = previous.get("results", [])
    latest_results = latest.get("results", [])

    def make_key(test):

        method = str(
            test.get("method", "")
        ).upper()

        endpoint = str(
            test.get("endpoint", "")
        )

        expected = test.get("expected")

        return "{} {} {}".format(
            method,
            endpoint,
            expected
        )

    previous_map = {}

    for test in previous_results:
        key = make_key(test)
        previous_map[key] = test

    latest_map = {}

    for test in latest_results:
        key = make_key(test)
        latest_map[key] = test

    regressions = []
    fixed = []
    still_failing = []

    for key in latest_map:

        if key not in previous_map:
            continue

        old = previous_map[key]
        current = latest_map[key]

        old_pass = old.get("passed", False)
        current_pass = current.get("passed", False)

        item = {
            "name": current.get("name", ""),
            "method": current.get("method", ""),
            "endpoint": current.get("endpoint", ""),
            "expected": current.get("expected"),
            "previous_status": old.get("status_code"),
            "current_status": current.get("status_code")
        }

        # PASS → FAIL
        if old_pass and not current_pass:
            regressions.append(item)

        # FAIL → PASS
        elif not old_pass and current_pass:
            fixed.append(item)

        # FAIL → FAIL
        elif not old_pass and not current_pass:
            still_failing.append(item)

    return {
        "current_run": latest.get("run_number"),
        "previous_run": previous.get("run_number"),
        "regressions": regressions,
        "fixed": fixed,
        "still_failing": still_failing
    }

@app.post("/run")
def run_tests():

    result = subprocess.run(
        [
            sys.executable,
            "backend/agent_workflow.py"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:

        return {
            "status": "error",
            "message": "Test execution failed.",
            "details": result.stderr
        }

    try:

        with open("backend/test_results.json", "r") as file:
            results = json.load(file)

        with open("backend/qa_report.json", "r") as file:
            report = json.load(file)

    except Exception as error:

        return {
            "status": "error",
            "message": "Test files could not be read.",
            "details": str(error)
        }

    total = report.get("total_tests", len(results))
    passed = report.get("passed", 0)
    failed = report.get("failed", 0)
    skipped = report.get("skipped", 0)

    if total > 0:
        pass_rate = round((passed / total) * 100)
    else:
        pass_rate = 0

    history = load_history()

    run_data = {
        "run_number": len(history) + 1,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "pass_rate": pass_rate,
        "results": []
    }

    for test in results:

        run_data["results"].append({
            "name": test.get("name", ""),
            "method": test.get("method", ""),
            "endpoint": test.get("endpoint", ""),
            "expected": test.get("expected"),
            "status_code": test.get("actual"),
            "response_time": test.get("response_time"),
            "passed": test.get("result") == "PASS"
        })

    history.append(run_data)

    save_history(history)

    return {
        "status": "success",
        "message": "Tests completed successfully.",
        "run_number": run_data["run_number"],
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": pass_rate
    }