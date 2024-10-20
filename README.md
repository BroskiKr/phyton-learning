# FastAPI Application with Posts and Users Data in PostgreSQL and MongoDB

This FastAPI application serves as a simple API for managing posts and users stored in PostgreSQL and MongoDB databases. It provides endpoints to retrieve, list, create, update, and delete posts and users. The application also supports authentication via JWT tokens and through your Google account, Discord bot integration, and asynchronous tasks using Celery.

# Prerequisites:
To run this FastAPI application, ensure you have Python, Docker, and Docker Compose installed on your system, along with the necessary libraries. Follow these steps:

1. Install Python from python.org if you haven't already.

2. Install poetry (packaging and dependency management):
`pip install poetry`

3. Install all requirements needed to start the application using poetry:
`poetry install`

4. Create `.env` file in the root of the project use `.env-template` as an example and set your PostgreSQL and MongoDB connection URLs and other values

# How to Run:

1. Clone or download this repository to your local machine.

2. Navigate to the project directory in your terminal.

3. Ensure you have Docker and Docker Compose installed on your machine and start the services using Docker Compose:
`docker-compose up -d`
This command will build and start the containers defined in your docker-compose.yml file.

4. You can also run the Discord bot that communicates with our API:
`poetry run python app/discord_bot/discord_bot.py`

5. Once the server starts successfully, you can access the API endpoints from your browser or API testing tools like Postman or curl.

6. You can also access Swagger for service here http://127.0.0.1:8000/docs

# Authentication:
The application supports JWT-based authentication and login via Google OAuth. Tokens must be included in the Authorization header as Bearer <token> for protected routes.

# Async Tasks:
Celery is used for managing asynchronous tasks like web scraping. These tasks are triggered by specific endpoints and run in the background using the Celery worker and celery beat.

# Tests:
The application includes tests for its endpoints using Pytest. To run the tests:
`poetry run pytest`

# Migrations:
Database migrations are managed using Alembic. Migrations are stored in the migrations directory. You can generate and apply migrations using the following Alembic commands:

Generate a new migration:
`alembic revision --autogenerate -m "migration_message"`

Apply migrations:
`alembic upgrade head`

Ensure that you review and customize the generated migration files before applying them to your database.

