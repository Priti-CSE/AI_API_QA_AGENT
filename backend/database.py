import psycopg2

def get_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="ai_api_qa",
        user="postgres",
        password="123456"
    )

    return connection


connection = get_connection()

print("PostgreSQL connected successfully.")

connection.close()