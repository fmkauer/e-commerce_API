from typing import Optional, List, Dict
from datetime import datetime, UTC
from .models import User, Order, Product
from .schemas import UserInDB, OrderCreate, ProductCreate
from .data import MOCK_USERS, MOCK_ORDERS, MOCK_PRODUCT, LAST_ORDER_ID

# In-memory database
users_db: Dict[int, dict] = {}
orders_db: Dict[int, dict] = {}
products_db: Dict[int, dict] = {}
last_order_id = LAST_ORDER_ID
last_product_id = 1  # Initialize with 1 since we have one mock product


def init_db():
    """Initialize the database with mock data"""
    # Initialize users
    for user in MOCK_USERS:
        users_db[user["id"]] = user

    # Initialize orders
    for order in MOCK_ORDERS:
        orders_db[order["id"]] = order

    # Initialize products
    products_db[MOCK_PRODUCT["id"]] = MOCK_PRODUCT


# User operations
def get_user_by_username(username: str) -> Optional[UserInDB]:
    for user in users_db.values():
        if user["username"] == username:
            return UserInDB(**user)
    return None


def get_user_by_id(user_id: int) -> Optional[UserInDB]:
    user = users_db.get(user_id)
    if user:
        return UserInDB(**user)
    return None


# Product operations
def get_product_by_id(product_id: int) -> Optional[Product]:
    product = products_db.get(product_id)
    if product:
        return Product(**product)
    return None


def get_all_products() -> List[Product]:
    return [Product(**product) for product in products_db.values()]


def create_product(product: ProductCreate) -> Product:
    global last_product_id
    last_product_id += 1
    
    # Create and validate the product before storing it
    new_product = Product(
        id=last_product_id,
        name=product.name,
        description=product.description,
        price=product.price
    )
    
    # If validation passes, store the product
    products_db[last_product_id] = new_product.model_dump()
    return new_product


# Order operations
def get_orders_by_user(user_id: int) -> List[Order]:
    return [
        add_product_details(Order(**order))
        for order in orders_db.values()
        if order["user_id"] == user_id
    ]


def get_order_by_id(order_id: int) -> Optional[Order]:
    order = orders_db.get(order_id)
    if order:
        return add_product_details(Order(**order))
    return None


def create_order(user_id: int, order: OrderCreate) -> Order:
    global last_order_id
    
    # Check if product exists
    product = get_product_by_id(order.product_id)
    if not product:
        raise ValueError("Product not found")
    
    last_order_id += 1
    new_order = {
        "id": last_order_id,
        "user_id": user_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "total_price": order.quantity * product.price,
        "status": "pending",
        "created_at": datetime.now(UTC),
        "updated_at": None
    }
    
    orders_db[last_order_id] = new_order
    return Order(**new_order)


def update_order_status(order_id: int, status: str) -> Optional[Order]:
    order = orders_db.get(order_id)
    if order:
        order["status"] = status
        order["updated_at"] = datetime.now(UTC)
        return Order(**order)
    return None


def get_all_orders() -> List[Order]:
    return [add_product_details(Order(**order)) for order in orders_db.values()]

def add_product_details(order: Order) -> Order:
    products = []
    for item in order.items:
        product = get_product_by_id(item.id)
        products.append(product)
    order.products = products
    return order