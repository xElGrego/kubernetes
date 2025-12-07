from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import httpx
import os

app = FastAPI(title="Orders API", version="1.0.0")

# URL del servicio de usuarios (DNS interno de Kubernetes)
USERS_API_URL = os.getenv("USERS_API_URL", "http://users-api:8000")


# Modelo de datos
class Order(BaseModel):
    id: int
    user_id: int
    product: str
    quantity: int
    total: float
    status: str
    created_at: str


class OrderWithUser(BaseModel):
    order: Order
    user: dict


# Base de datos simulada de pedidos
ORDERS_DB = [
    Order(
        id=101,
        user_id=1,
        product="Laptop Dell XPS",
        quantity=1,
        total=1299.99,
        status="delivered",
        created_at="2024-05-01",
    ),
    Order(
        id=102,
        user_id=2,
        product="Mouse Logitech",
        quantity=2,
        total=49.98,
        status="shipped",
        created_at="2024-05-15",
    ),
    Order(
        id=103,
        user_id=1,
        product="Teclado Mecánico",
        quantity=1,
        total=129.99,
        status="processing",
        created_at="2024-06-01",
    ),
    Order(
        id=104,
        user_id=3,
        product="Monitor 27 pulgadas",
        quantity=1,
        total=399.99,
        status="delivered",
        created_at="2024-06-10",
    ),
    Order(
        id=105,
        user_id=4,
        product="Webcam HD",
        quantity=1,
        total=79.99,
        status="pending",
        created_at="2024-06-20",
    ),
]


@app.get("/")
def health_check():
    """Health check endpoint"""
    return {
        "service": "orders-api",
        "status": "healthy",
        "users_api_url": USERS_API_URL,
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/orders", response_model=List[Order])
def get_all_orders():
    """Obtener todos los pedidos"""
    return ORDERS_DB


@app.get("/orders/{order_id}", response_model=Order)
def get_order_by_id(order_id: int):
    """Obtener un pedido específico por ID"""
    order = next((o for o in ORDERS_DB if o.id == order_id), None)
    if not order:
        raise HTTPException(
            status_code=404, detail=f"Pedido con ID {order_id} no encontrado"
        )
    return order


@app.get("/orders/{order_id}/details", response_model=OrderWithUser)
async def get_order_with_user(order_id: int):
    """
    Obtener pedido con información del usuario
    Este endpoint demuestra la comunicación entre microservicios vía DNS de Kubernetes
    """
    # Buscar el pedido
    order = next((o for o in ORDERS_DB if o.id == order_id), None)
    if not order:
        raise HTTPException(
            status_code=404, detail=f"Pedido con ID {order_id} no encontrado"
        )

    # Llamar al servicio de usuarios usando DNS interno de Kubernetes
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{USERS_API_URL}/users/{order.user_id}")

            if response.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail=f"Usuario con ID {order.user_id} no encontrado",
                )

            response.raise_for_status()
            user_data = response.json()

        return OrderWithUser(order=order, user=user_data)

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Error al comunicarse con users-api: {str(e)}"
        )


@app.get("/orders/user/{user_id}", response_model=List[Order])
def get_orders_by_user(user_id: int):
    """Obtener todos los pedidos de un usuario específico"""
    user_orders = [o for o in ORDERS_DB if o.user_id == user_id]
    if not user_orders:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron pedidos para el usuario {user_id}",
        )
    return user_orders


@app.get("/orders/user/{user_id}/full")
async def get_user_orders_with_details(user_id: int):
    """
    Obtener pedidos de un usuario con su información completa
    Demuestra múltiples llamadas al servicio de usuarios
    """
    # Buscar pedidos del usuario
    user_orders = [o for o in ORDERS_DB if o.user_id == user_id]
    if not user_orders:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron pedidos para el usuario {user_id}",
        )

    # Obtener información del usuario
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{USERS_API_URL}/users/{user_id}")

            if response.status_code == 404:
                raise HTTPException(
                    status_code=404, detail=f"Usuario con ID {user_id} no encontrado"
                )

            response.raise_for_status()
            user_data = response.json()

        return {
            "user": user_data,
            "orders": user_orders,
            "total_orders": len(user_orders),
            "total_spent": sum(o.total for o in user_orders),
        }

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Error al comunicarse con users-api: {str(e)}"
        )


@app.get("/health")
async def detailed_health():
    """Endpoint de salud detallado que verifica conectividad con users-api"""
    users_api_status = "unknown"

    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"{USERS_API_URL}/health")
            if response.status_code == 200:
                users_api_status = "healthy"
            else:
                users_api_status = "unhealthy"
    except:
        users_api_status = "unreachable"

    return {
        "service": "orders-api",
        "status": "healthy",
        "total_orders": len(ORDERS_DB),
        "users_api_connection": users_api_status,
        "users_api_url": USERS_API_URL,
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
