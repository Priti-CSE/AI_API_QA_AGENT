import redis

client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

client.set("test_key", "Redis is working")

value = client.get("test_key")

print(value)

client.delete("test_key")