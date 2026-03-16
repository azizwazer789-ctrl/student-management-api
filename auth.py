from fastapi import HTTPException
from database import users_db

def authenticate_user(username: str, password: str):

    if username not in users_db:
        raise HTTPException(
            status_code=401,
            detail="Invalid username"
        )

    if users_db[username] != password:
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    return True