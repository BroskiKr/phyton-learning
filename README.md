# FastAPI Application with Posts and Users Data in PostgreSQL DB

This FastAPI application serves as a simple API for accessing posts and users stored in a PostgreSQL database. It provides endpoints to retrieve individual posts and users, list all of them, create, update and delete them.

# Prerequisites:
To run this FastAPI application, you need to have Python installed on your system along with the necessary libraries. Follow these steps:

1. Install Python from python.org if you haven't already.

2. Install FastAPI, Uvicorn (ASGI server), psycopg2 (PostgreSQL adapter), sqlalchemy, and alembic for managing database migrations using pip:
`pip install fastapi uvicorn psycopg2 sqlalchemy alembic`


# How to Run:

1. Clone or download this repository to your local machine.

2. Navigate to the project directory in your terminal.

3. In file 'alembic.ini' find the line `sqlalchemy.url = ... `
and set the path to your local database

OR

3.1 Install python-dotenv and create `.env` file in the root of the project use `.env-template` as an example and set your PostgreSQL connection URL   
`pip install python-dotenv` 

4. Apply database migrations using alembic:
`alembic upgrade head`

5. Run the FastAPI application using Uvicorn:
`uvicorn main:app --reload`

6. Once the server starts successfully, you can access the API endpoints from your browser or API testing tools like Postman or curl.

7. You can also access Swagger for service here http://127.0.0.1:8000/docs

# Migrations:
Database migrations are managed using Alembic. Migrations are stored in the migrations directory. You can generate and apply migrations using the following Alembic commands:

Generate a new migration:
`alembic revision --autogenerate -m "migration_message"`

Apply migrations:
`alembic upgrade head`

Ensure that you review and customize the generated migration files before applying them to your database.

