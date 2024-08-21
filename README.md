# FastAPI Application with Posts and Users Data in PostgreSQL and MongoDB

This FastAPI application serves as a simple API for accessing posts and users stored in a PostgreSQL and MongoDb databases. It provides endpoints to retrieve individual posts and users, list all of them, create, update and delete them.

# Prerequisites:
To run this FastAPI application, you need to have Python installed on your system along with the necessary libraries. Follow these steps:

1. Install Python from python.org if you haven't already.

2. Install poetry (packaging and dependency management):
`pip install poetry`

3. Install all requirements needed to start the application using poetry:
`poetry install`

4. Create `.env` file in the root of the project use `.env-template` as an example and set your PostgreSQL and MongoDB connection URLs and SECRET_KEY for jwt auth  

# How to Run:

1. Clone or download this repository to your local machine.

2. Navigate to the project directory in your terminal.

3. Ensure you have Docker and Docker Compose installed on your machine and start the services using Docker Compose:
`docker-compose up -d`
This command will build and start the containers defined in your docker-compose.yml file.

4. Apply database migrations using alembic:
`alembic upgrade head`

5. Start celery worker and celery beat for async tasks:
`celery -A app.tasks:celery beat -S redbeat.RedBeatScheduler --max-interval 30 --loglevel=info -l debug`
`celery -A app.tasks:celery worker --loglevel=info --pool=solo`

6. Run the FastAPI application using Uvicorn:
`uvicorn app.main:app --reload`

7. Once the server starts successfully, you can access the API endpoints from your browser or API testing tools like Postman or curl.

8. You can also access Swagger for service here http://127.0.0.1:8000/docs

# Migrations:
Database migrations are managed using Alembic. Migrations are stored in the migrations directory. You can generate and apply migrations using the following Alembic commands:

Generate a new migration:
`alembic revision --autogenerate -m "migration_message"`

Apply migrations:
`alembic upgrade head`

Ensure that you review and customize the generated migration files before applying them to your database.

