import json
import psycopg2


def get_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="ai_api_qa",
        user="postgres",
        password="123456"
    )

    return connection


with open("backend/test_results.json", "r") as file:
    results = json.load(file)


connection = get_connection()
cursor = connection.cursor()


for result in results:

    cursor.execute(
        """
        INSERT INTO test_results
        (test_name, method, endpoint, expected_status, actual_status, result)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            result["name"],
            result["method"],
            result["endpoint"],
            result["expected"],
            result["actual"],
            result["result"]
        )
    )


connection.commit()

cursor.close()
connection.close()

print("Test results saved to PostgreSQL successfully.")