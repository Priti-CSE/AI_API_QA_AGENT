from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="User Management API")

class User(BaseModel):
    name: str
    email: str

users = [
    {"id": 1, "name": "Priti", "email": "priti@example.com"},
    {"id": 2, "name": "Rahul", "email": "rahul@example.com"}
]


@app.get("/")
def home():
    return {"message": "User Management API is running"}


@app.get("/users")
def get_users():
    return users

@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user

    raise HTTPException(status_code=404, detail="User not found")

@app.post("/users")
def create_user(user: User):
    new_user = {
        "id": len(users) + 1,
        "name": user.name,
        "email": user.email
    }

    users.append(new_user)

    return new_user

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    for existing_user in users:
        if existing_user["id"] == user_id:
            existing_user["name"] = user.name
            existing_user["email"] = user.email
            return existing_user

    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return {"message": "User deleted successfully"}

    raise HTTPException(status_code=404, detail="User not found")