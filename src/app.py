from contextlib import asynccontextmanager
from datetime import timedelta
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from .auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_active_user,
    get_user_by_username,
    verify_password,
)
from .database import (
    create_order,
    create_product,
    get_all_orders,
    get_all_products,
    get_order_by_id,
    get_orders_by_user,
    get_product_by_id,
    init_db,
    update_order_status,
    delete_product_by_id,
)
from .models import Order, Product, User
from .schemas import (
    OrderCreate,
    OrderResponse,
    ProductCreate,
    ProductResponse,
    Token,
    UserInDB,
    ChatMessage,
)
from candidate_solution.solution import generate_answer


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database with mock data on startup
    init_db()
    yield


app = FastAPI(
    title="E-commerce Mock API",
    description="A mock e-commerce API built with FastAPI",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/login", response_model=Token, tags=["Authentication"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate user and return JWT token.

    - **username**: Username for authentication
    - **password**: Password for authentication
    """
    user = get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/products", response_model=List[ProductResponse], tags=["Products"])
async def read_products(current_user: UserInDB = Depends(get_current_active_user)):
    """
    Get all products.

    Returns a list of all available products in the store.
    """
    return get_all_products()


@app.get("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
async def read_product(
    product_id: int, current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Get a specific product by ID.

    - **product_id**: The ID of the product to retrieve
    """
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products", response_model=ProductResponse, tags=["Products"])
async def create_new_product(
    product: ProductCreate, current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Create a new product (admin only).

    - **name**: Product name
    - **description**: Product description
    - **price**: Product price (must be greater than 0)
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create products",
        )
    return create_product(product)


@app.get("/orders", response_model=List[OrderResponse], tags=["Orders"])
async def read_orders(current_user: UserInDB = Depends(get_current_active_user)):
    """
    Get all orders for the current user.

    Returns a list of all orders placed by the authenticated user.
    Admin users can see all orders.
    """
    if current_user.role != "admin":
        return get_orders_by_user(current_user.id)
    else:
        return get_all_orders()


@app.get("/user_orders", response_model=List[OrderResponse], tags=["Orders"])
async def read_user_orders(
    user_id: int, current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Get all orders for the a specific user. Admin only.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Not authorized to access this order"
        )
    return get_orders_by_user(user_id)


@app.get("/orders/{order_id}", response_model=OrderResponse, tags=["Orders"])
async def read_order(
    order_id: int, current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Get a specific order by ID.

    - **order_id**: The ID of the order to retrieve

    Note: Users can only access their own orders. Admin users can access any order.
    """
    order = get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Not authorized to access this order"
        )
    return order


@app.post("/orders", response_model=OrderResponse, tags=["Orders"])
async def create_new_order(
    order: OrderCreate, current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Create a new order for the current user.

    - **product_id**: ID of the product to order
    - **quantity**: Number of items to order (must be greater than 0)
    """
    return create_order(current_user.id, order)


@app.post("/create_order", response_model=OrderResponse, tags=["Orders"])
async def create_order(
    user_id: int,
    order: OrderCreate,
    current_user: UserInDB = Depends(get_current_active_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to create an order")
    return create_order(user_id, order)


@app.post("/orders/{order_id}/cancel", response_model=OrderResponse, tags=["Orders"])
async def cancel_order(
    order_id: int, current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Cancel a specific order.

    - **order_id**: The ID of the order to cancel

    Notes:
    - Users can only cancel their own orders
    - Admin users can cancel any order
    - Cannot cancel orders that have been delivered
    """
    order = get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Not authorized to cancel this order"
        )
    if order.status == "delivered":
        raise HTTPException(status_code=400, detail="Cannot cancel a delivered order")

    updated_order = update_order_status(order_id, "cancelled")
    if not updated_order:
        raise HTTPException(status_code=500, detail="Failed to update order status")
    return updated_order


@app.delete("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
async def delete_product(
    product_id: int, current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Delete a specific product by ID.

    Can only be done by admin users. And can't delete products that have been ordered.
    """
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    all_orders = get_all_orders()
    for order in all_orders:
        if product_id in [item.id for item in order.items]:
            raise HTTPException(
                status_code=400, detail="Cannot delete a product that has been ordered"
            )
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this product"
        )
    delete_product_by_id(product_id)
    return product


@app.post("/chat", response_model=List[ChatMessage], tags=["Chat"])
async def chat(
    user_id: int,
    messages: List[ChatMessage],
):
    return generate_answer(user_id, messages)  #  use candidate_solution/solution.py
