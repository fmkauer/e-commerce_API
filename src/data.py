from datetime import UTC, datetime, timedelta

from passlib.context import CryptContext

from .models import Item, OrderStatus, Product

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Create mock product using the Product model
MOCK_PRODUCTS = [
    Product(
        id=1,
        name="Classic White T-Shirt",
        description="A comfortable cotton t-shirt perfect for everyday wear",
        price=19.99
    ).model_dump(),
    Product(
        id=2,
        name="Slim Fit Jeans",
        description="Modern slim fit denim jeans with stretch comfort technology",
        price=49.99
    ).model_dump(),
    Product(
        id=3,
        name="Running Shoes Pro",
        description="Lightweight athletic shoes with enhanced cushioning and support",
        price=89.99
    ).model_dump(),
    Product(
        id=4,
        name="Leather Wallet",
        description="Genuine leather bifold wallet with RFID protection",
        price=29.99
    ).model_dump(),
    Product(
        id=5,
        name="Wireless Headphones",
        description="Bluetooth headphones with noise cancellation and 20-hour battery life",
        price=129.99
    ).model_dump(),
    Product(
        id=6,
        name="Backpack Deluxe",
        description="Water-resistant backpack with laptop compartment and USB charging port",
        price=59.99
    ).model_dump(),
    Product(
        id=7,
        name="Smart Watch Sport",
        description="Fitness tracker with heart rate monitor and GPS",
        price=199.99
    ).model_dump(),
    Product(
        id=8,
        name="Sunglasses Classic",
        description="UV protection sunglasses with polarized lenses",
        price=79.99
    ).model_dump(),
    Product(
        id=9,
        name="Winter Jacket",
        description="Waterproof insulated jacket with removable hood",
        price=149.99
    ).model_dump(),
    Product(
        id=10,
        name="Canvas Sneakers",
        description="Casual canvas sneakers perfect for any occasion",
        price=39.99
    ).model_dump()
]

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
        "email": "john.doe@example.com",
        "username": "johndoe",
        "hashed_password": get_password_hash("password123"),
        "role": "user"
    },
    {
        "id": 3,
        "email": "sarah.smith@example.com",
        "username": "sarahs",
        "hashed_password": get_password_hash("userpass456"),
        "role": "user"
    },
    {
        "id": 4,
        "email": "michael.brown@example.com",
        "username": "mikebrown",
        "hashed_password": get_password_hash("securepass789"),
        "role": "user"
    },
    {
        "id": 5,
        "email": "emma.wilson@example.com",
        "username": "emmaw",
        "hashed_password": get_password_hash("emma2024!"),
        "role": "user"
    },
    {
        "id": 6,
        "email": "david.miller@example.com",
        "username": "davidm",
        "hashed_password": get_password_hash("miller#pass"),
        "role": "user"
    }
]

# Generate timestamps for mock orders
now = datetime.now(UTC)
MOCK_ORDERS = [
    {
        "id": 1,
        "user_id": 2,  # John Doe
        "items": [
            {"id": 1, "quantity": 2},  # T-shirts
            {"id": 4, "quantity": 1}   # Wallet
        ],
        "total_price": 69.97,  # (19.99 * 2) + 29.99
        "status": OrderStatus.DELIVERED,
        "created_at": now - timedelta(days=30),
        "updated_at": now - timedelta(days=25),
        "delivery_date": (now - timedelta(days=23))
    },
    {
        "id": 2,
        "user_id": 3,  # Sarah Smith
        "items": [
            {"id": 5, "quantity": 1},  # Wireless Headphones
            {"id": 7, "quantity": 1}   # Smart Watch
        ],
        "total_price": 329.98,  # 129.99 + 199.99
        "status": OrderStatus.SHIPPED,
        "created_at": now - timedelta(days=15),
        "updated_at": now - timedelta(days=13),
        "delivery_date": (now - timedelta(days=8))
    },
    {
        "id": 3,
        "user_id": 4,  # Michael Brown
        "items": [
            {"id": 2, "quantity": 2},  # Jeans
            {"id": 10, "quantity": 1}  # Canvas Sneakers
        ],
        "total_price": 139.97,  # (49.99 * 2) + 39.99
        "status": OrderStatus.PENDING,
        "created_at": now - timedelta(days=1),
        "updated_at": None,
        "delivery_date": (now + timedelta(days=6))
    },
    {
        "id": 4,
        "user_id": 5,  # Emma Wilson
        "items": [
            {"id": 9, "quantity": 1},  # Winter Jacket
            {"id": 8, "quantity": 1}   # Sunglasses
        ],
        "total_price": 229.98,  # 149.99 + 79.99
        "status": OrderStatus.PROCESSING,
        "created_at": now - timedelta(days=5),
        "updated_at": now - timedelta(days=4),
        "delivery_date": (now + timedelta(days=2))
    },
    {
        "id": 5,
        "user_id": 6,  # David Miller
        "items": [
            {"id": 3, "quantity": 1},  # Running Shoes
            {"id": 6, "quantity": 1}   # Backpack
        ],
        "total_price": 149.98,  # 89.99 + 59.99
        "status": OrderStatus.CANCELLED,
        "created_at": now - timedelta(days=10),
        "updated_at": now - timedelta(days=9),
        "delivery_date": (now - timedelta(days=3))
    },
    {
        "id": 6,
        "user_id": 2,  # John Doe
        "items": [
            {"id": 7, "quantity": 1},  # Smart Watch
            {"id": 5, "quantity": 1}   # Wireless Headphones
        ],
        "total_price": 329.98,  # 199.99 + 129.99
        "status": OrderStatus.DELIVERED,
        "created_at": now - timedelta(days=45),
        "updated_at": now - timedelta(days=40),
        "delivery_date": (now - timedelta(days=45)) + timedelta(days=7)
    },
    {
        "id": 7,
        "user_id": 3,  # Sarah Smith
        "items": [
            {"id": 10, "quantity": 2},  # Canvas Sneakers
            {"id": 1, "quantity": 3}    # T-shirts
        ],
        "total_price": 139.95,  # (39.99 * 2) + (19.99 * 3)
        "status": OrderStatus.CANCELLED,
        "created_at": now - timedelta(days=25),
        "updated_at": now - timedelta(days=20),
        "delivery_date": (now - timedelta(days=18))
    },
    {
        "id": 8,
        "user_id": 4,  # Michael Brown
        "items": [
            {"id": 8, "quantity": 1},  # Sunglasses
            {"id": 4, "quantity": 2}   # Wallet
        ],
        "total_price": 139.97,  # 79.99 + (29.99 * 2)
        "status": OrderStatus.PROCESSING,
        "created_at": now - timedelta(days=2),
        "updated_at": now - timedelta(days=1),
        "delivery_date": (now + timedelta(days=5))
    },
    {
        "id": 9,
        "user_id": 2,  # John Doe
        "items": [
            {"id": 3, "quantity": 1},  # Running Shoes
            {"id": 8, "quantity": 1}   # Sunglasses
        ],
        "total_price": 169.98,  # 89.99 + 79.99
        "status": OrderStatus.PROCESSING,
        "created_at": now - timedelta(days=10),
        "updated_at": now - timedelta(days=8),
        "delivery_date": (now - timedelta(days=3))  # Expected 3 days ago but still processing
    }
]

LAST_ORDER_ID = 9  # Updated to reflect the new last order ID 