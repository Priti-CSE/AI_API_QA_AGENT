import json


def create_report():

    with open("backend/test_results.json", "r") as file:
        results = json.load(file)

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

    report = {
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped
    }

    with open("backend/qa_report.json", "w") as file:
        json.dump(report, file, indent=4)

    print("QA report created successfully.")
    print("Total tests:", total)
    print("Passed:", passed)
    print("Failed:", failed)
    print("Skipped:", skipped)


create_report()