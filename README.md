# E-commerce API

Welcome to the E-commerce API project! This project is designed to provide a comprehensive backend solution for managing customers, customer accounts, products, and orders in an e-commerce platform. The API is built using Flask, Flask-SQLAlchemy, and Marshmallow for serialization.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
  - [Customer Management](#customer-management)
  - [Customer Account Management](#customer-account-management)
  - [Product Catalog](#product-catalog)
  - [Order Processing](#order-processing)
- [Bonus Features](#bonus-features)
- [Database Integration](#database-integration)
- [Data Validation and Error Handling](#data-validation-and-error-handling)
- [Postman Collections](#postman-collections)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Customer Management**: CRUD operations for managing customers.
- **Customer Account Management**: CRUD operations for managing customer accounts.
- **Product Catalog**: CRUD operations for managing products.
- **Order Processing**: Comprehensive order management functionality.
- **Bonus Features**: Additional functionalities like managing product stock levels, restocking products, order history, order cancellation, and calculating order total price.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/CamHirsch23/E-commerce-API.git
    cd E-commerce-API
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**:
    - Ensure you have MySQL installed and running.
    - Create a database named `ecommerce_db`.
    - Update the `SQLALCHEMY_DATABASE_URI` in `app.py` with your MySQL credentials.

5. **Run the application**:
    ```bash
    python app.py
    ```

## Usage

Use Postman or any other API testing tool to interact with the API. The base URL for the API is `http://localhost:5000`.

## API Endpoints

### Customer Management

- **Create Customer**: `POST /customer`
- **Read Customer**: `GET /customer/<int:id>`
- **Update Customer**: `PUT /customer/<int:id>`
- **Delete Customer**: `DELETE /customer/<int:id>`

### Customer Account Management

- **Create Customer Account**: `POST /customer_account`
- **Read Customer Account**: `GET /customer_account/<int:id>`
- **Update Customer Account**: `PUT /customer_account/<int:id>`
- **Delete Customer Account**: `DELETE /customer_account/<int:id>`

### Product Catalog

- **Create Product**: `POST /product`
- **Read Product**: `GET /product/<int:id>`
- **Update Product**: `PUT /product/<int:id>`
- **Delete Product**: `DELETE /product/<int:id>`
- **List Products**: `GET /products`

### Order Processing

- **Place Order**: `POST /order`
- **Retrieve Order**: `GET /order/<int:id>`
- **Track Order**: `GET /order/<int:id>/status`
- **Order History**: `GET /customer/<int:customer_id>/orders`
- **Cancel Order**: `PUT /order/<int:id>/cancel`
- **Calculate Order Total**: `GET /order/<int:id>/total`

## Bonus Features

- **View and Manage Product Stock Levels**: `GET /product/<int:id>/stock`, `PUT /product/<int:id>/stock`
- **Restock Products When Low**: Implement logic to monitor and restock products.

## Database Integration

The application uses Flask-SQLAlchemy to integrate with a MySQL database. Ensure proper database connections and interactions for data storage and retrieval.

## Data Validation and Error Handling

The application implements data validation mechanisms to ensure that user inputs meet specified criteria (e.g., valid email addresses, proper formatting). Error handling is done using try, except, else, and finally blocks to provide informative error messages.

## Postman Collections

Develop Postman collections that categorize and group API requests according to their functionality. Separate collections for Customer Management, Product Management, Order Management, and Bonus Features should be created for clarity.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
