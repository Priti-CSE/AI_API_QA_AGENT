import redis
import json

client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


def save_results(results):
    client.set(
        "latest_test_results",
        json.dumps(results)
    )


def get_results():
    data = client.get("latest_test_results")

    if data is None:
        return None

    return json.loads(data)


print("Redis cache utility is ready.")