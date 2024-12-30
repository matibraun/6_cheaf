Inventory App README


Inventory Management Application

This application helps manage an inventory system, tracking product expiration dates, and notifying users about products that are near their expiration date. It includes the ability to set alerts, and it features a cron job to notify users when the alert conditions are met, and display all the active alerts.


Table of Contents

Prerequisites
Setup Instructions
PostgreSQL Setup
Application Setup
Endpoints And Sample Payloads
-Users App Endpoints
-Products App Endpoints
-Alerts App Endpoints
Scheduled Tasks


Prerequisites

Before running the application, ensure you have the following tools installed.

Docker
Docker Compose
PostgreSQL

The application uses PostgreSQL as the database. Ensure you set up PostgreSQL with the following credentials:

Database Name: postgres_db
User: postgres
Password: postgres
Host: 0.0.0.0
Port: 5432

PostgreSQL Setup

You can set up the PostgreSQL database via the command line:

bash
Copy code
psql -U postgres
CREATE DATABASE postgres_db;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE postgres_db TO postgres;
\q

Ensure the host is set to 0.0.0.0 to allow external connections. You can also configure this through a database management tool like DBeaver or pgAdmin.


Application Setup

Clone the repository:

git clone https://github.com/matibraun/6_cheaf.git
cd 6_cheaf

Build and run the application using Docker:

docker-compose up --build

The development server will be accessible at http://localhost:8000


Endpoints

Endpoint  //  HTTP Method  //  Description

Users App Endpoints

http://localhost:8000/users/register/  // POST  //	 Register a new user

Sample payload:

{
    "username": "newuser",
    "password": "newpassword",
    "email": "newuser@example.com",
    "first_name": "New",
    "last_name": "User"
}


http://localhost:8000/users/login/  // 	POST  //  User login and authentication

Sample payload:

{
    "username": "newuser",
    "password": "newpassword",
}

Once logged in, you will receive a token. Include this token in the headers for any authenticated requests.


The following endpoints are protected and need authentication. The token provided upon login must be incudded in the headers of the request.

Authorization: Token <token>


Products App Endpoints

http://localhost:8000/products/  //  POST  //  Create a new product

Sample payload:

{
    "name": "palta",
    "description": "aksjdkj",
    "stock_quantity": 62,
    "expiration_date": "2025-01-02"
}

Note: When creating a product, two alerts are automatically generated—one for 10 days before expiration, and another for 5 days before expiration.

http://localhost:8000/products/  //  GET  //  List all products

Note: This endpoint allows filtering thru name, description, min_stock and max_stock (http://localhost:8000/products/?name=palta)

http://localhost:8000/products/<int:pk>/  //  GET  //  Retrieve specific product by id

http://localhost:8000/products/<int:pk>/alerts/  //  GET  //  Retrieve all the alerts fo specific product by id

http://localhost:8000/products/filter-by-dates/?start_date=2025-03-14&end_date=2025-05-14  //  GET  //  List all the products with expiration_date between the specified dates

http://localhost:8000/products/filter-by-days/?days=10  //  GET  //  List all the products with expiration_date within the next specified days

http://localhost:8000/products/filter-by-alert-status/?status=active  //  GET  //  List all the products containing alerts with the specified status ['active', 'expired']

http://localhost:8000/products/<int:pk>/  //  PATCH  //  Update specific product by id

http://localhost:8000/products/<int:pk>/  //  DELETE  //  Delete specific product by id


Alerts App Endpoints

http://localhost:8000/alerts/  //  POST  //  Create a new alert

Sample payload:

{
    "product_id": 4,
    "days_before_expiration_to_trigger": 7
}

http://localhost:8000/alerts/  //  GET  //  List all alerts

http://localhost:8000/alerts/<int:pk>/  //  GET  //  Retrieve specific alert by id

http://localhost:8000/alerts/filter-by-status/?status=active  //  GET  //  List all the alerts with the specified status ['active', 'expired']

http://localhost:8000/alerts/<int:pk>/  //  PATCH  //  Update specific alert by id

http://localhost:8000/alerts/<int:pk>/  //  DELETE  //  Delete specific alert by id


Scheduled Tasks

The application runs the following scheduled tasks every day:

7 PM: Displays all products with active alerts.
8 PM: Sends an email to each user for products with alerts triggered for the current date (mocked).
