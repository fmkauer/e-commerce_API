# E-commerce Mock API

A mock e-commerce API built with FastAPI that simulates a simple order management system.

## Features

- User authentication with JWT tokens
- Order management (create, view, cancel)
- Role-based access control (admin vs regular users)
- Mock product data
- In-memory database for testing

## Prerequisites

- Python 3.12+
- Poetry (for dependency management)

## Installation

1. Clone the repository
2. Create a virtual environment:

   On Unix-based systems:
   ```bash
   python3 -m venv .venv
   ```

   On Windows:
   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:

   On Unix-based systems:
   ```bash
   source .venv/bin/activate
   ```

   On Windows:
   ```bash
   .venv\Scripts\activate
   ```

4. Upgrade pip:
   ```bash
   pip install --upgrade pip
   ```

5. Install Poetry:
   ```bash
   pip install poetry
   ```

3. Install project dependencies using Poetry:
   ```bash
   poetry install
   ```

## Running the API

1. Activate the virtual environment:
   ```bash
   poetry shell
   ```

2. Start the server:
   ```bash
   uvicorn src.app:app --reload
   ```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

### Using Swagger UI Authorization

1. Click on the "Authorize" button (🔓) at the top right of the Swagger UI page
2. In the login form:
   - Enter any of the mock user credentials (e.g., username: `johndoe`, password: `password123`)
   - Click "Authorize"
3. The system will automatically:
   - Call the login endpoint
   - Include the JWT token in all subsequent API requests
4. You can now test any endpoint directly from the Swagger UI

## Available Endpoints

### Authentication
- `POST /login` - Authenticate user and get JWT token

### Orders
- `GET /orders` - Get all orders for the current user
- `POST /orders` - Create a new order
- `GET /orders/{order_id}` - Get a specific order by ID
- `POST /orders/{order_id}/cancel` - Cancel a specific order

## Mock Users

The API comes with three pre-configured users:

1. Admin User
   - Username: admin
   - Password: admin123

2. Regular User 1
   - Username: johndoe
   - Password: password123

3. Regular User 2
   - Username: sarahs
   - Password: userpass456

## Mock Products

The API comes with several products. Here are two examples:

1. Classic White T-Shirt
   - ID: 1
   - Price: $19.99
   - Description: A comfortable cotton t-shirt perfect for everyday wear

2. Wireless Headphones
   - ID: 5
   - Price: $129.99
   - Description: Bluetooth headphones with noise cancellation and 20-hour battery life

## Example Usage

1. First, get a JWT token by logging in:
   ```bash
   curl -X POST "http://localhost:8000/login" \
   -H "Content-Type: application/x-www-form-urlencoded" \
   -d "username=user1&password=user123"
   ```

   This will return a response like:
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "token_type": "bearer"
   }
   ```

2. Use the JWT token from the response to create a new order:
   ```bash
   # Replace the JWT_TOKEN with the access_token from the login response
   export JWT_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

   curl -X POST "http://localhost:8000/orders" \
   -H "Authorization: Bearer $JWT_TOKEN" \
   -H "Content-Type: application/json" \
   -d '{
     "items": [
       {
         "product_id": 1,
         "quantity": 2
       }
     ]
   }'
   ```

3. View all orders using the same JWT token:
   ```bash
   curl "http://localhost:8000/orders" \
   -H "Authorization: Bearer $JWT_TOKEN"
   ```

4. Get details of a specific product:
   ```bash
   curl "http://localhost:8000/products/1" \
   -H "Authorization: Bearer $JWT_TOKEN"
   ```
