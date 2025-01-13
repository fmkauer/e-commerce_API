from datetime import datetime, timedelta, UTC
from .models import OrderStatus, Product, Item
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Create mock product using the Product model
MOCK_PRODUCT = Product(
    id=1,
    name="Classic White T-Shirt",
    description="A comfortable cotton t-shirt perfect for everyday wear",
    price=19.99
).model_dump()  # Convert to dictionary for consistency with other mock data

MOCK_USERS = [
    {
        "id": 1,
        "email": "admin@example.com",
        "username": "admin",
        "hashed_password": get_password_hash("admin123"),
        "role": "admin"
    },
    {
        "id": 2,
        "email": "user1@example.com",
        "username": "user1",
        "hashed_password": get_password_hash("user123"),
        "role": "user"
    },
    {
        "id": 3,
        "email": "user2@example.com",
        "username": "user2",
        "hashed_password": get_password_hash("user456"),
        "role": "user"
    }
]

# Generate timestamps for mock orders
now = datetime.now(UTC)
MOCK_ORDERS = [
    {
        "id": 1,
        "user_id": 2,
        "items": [
            {"id": 1, "quantity": 2}
        ],
        "total_price": 39.98,
        "status": OrderStatus.DELIVERED,
        "created_at": now - timedelta(days=30),
        "updated_at": now - timedelta(days=25)
    },
    {
        "id": 2,
        "user_id": 2,
        "items": [
            {"id": 1, "quantity": 1}
        ],
        "total_price": 19.99,
        "status": OrderStatus.SHIPPED,
        "created_at": now - timedelta(days=15),
        "updated_at": now - timedelta(days=13)
    },
    {
        "id": 3,
        "user_id": 2,
        "items": [
            {"id": 1, "quantity": 3}
        ],
        "total_price": 59.97,
        "status": OrderStatus.PENDING,
        "created_at": now - timedelta(days=1),
        "updated_at": None
    },
    {
        "id": 4,
        "user_id": 3,
        "items": [
            {"id": 1, "quantity": 1}
        ],
        "total_price": 19.99,
        "status": OrderStatus.DELIVERED,
        "created_at": now - timedelta(days=20),
        "updated_at": now - timedelta(days=15)
    },
    {
        "id": 5,
        "user_id": 3,
        "items": [
            {"id": 1, "quantity": 2}
        ],
        "total_price": 39.98,
        "status": OrderStatus.CANCELLED,
        "created_at": now - timedelta(days=10),
        "updated_at": now - timedelta(days=9)
    },
    {
        "id": 6,
        "user_id": 3,
        "items": [
            {"id": 1, "quantity": 1}
        ],
        "total_price": 19.99,
        "status": OrderStatus.PROCESSING,
        "created_at": now - timedelta(days=2),
        "updated_at": now - timedelta(days=1)
    }
]

LAST_ORDER_ID = 6  # Used for generating new order IDs 