import secrets
import string

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

def generate_secure_password(length: int = 10) -> str:
    """Генерирует криптографически безопасный пароль заданной длины."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"

    while True:
        password = ''.join(secrets.choice(characters) for _ in range(length))
        # Гарантируем наличие хотя бы одного символа каждого типа
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in "!@#$%^&*" for c in password)):
            return password
        
@app.get("/random")
def get_secure_password():
    """Возвращает криптографически безопасный 10-значный пароль"""
    return {"secure_password": generate_secure_password(10)}