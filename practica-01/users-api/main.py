from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Users API", version="1.0.0")


# Modelo de datos
class User(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: str


# Base de datos simulada
USERS_DB = [
    User(
        id=1,
        name="Juan Pérez",
        email="juan@example.com",
        role="customer",
        created_at="2024-01-15",
    ),
    User(
        id=2,
        name="María García",
        email="maria@example.com",
        role="customer",
        created_at="2024-02-20",
    ),
    User(
        id=3,
        name="Carlos López",
        email="carlos@example.com",
        role="admin",
        created_at="2024-03-10",
    ),
    User(
        id=4,
        name="Ana Martínez",
        email="ana@example.com",
        role="customer",
        created_at="2024-04-05",
    ),
]


@app.get("/")
def health_check():
    """Health check endpoint"""
    return {
        "service": "users-api",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/users", response_model=List[User])
def get_all_users():
    """Obtener todos los usuarios"""
    return USERS_DB


@app.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: int):
    """Obtener un usuario específico por ID"""
    user = next((u for u in USERS_DB if u.id == user_id), None)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"Usuario con ID {user_id} no encontrado"
        )
    return user


@app.get("/health")
def detailed_health():
    """Endpoint de salud detallado"""
    return {
        "service": "users-api",
        "status": "healthy",
        "total_users": len(USERS_DB),
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
