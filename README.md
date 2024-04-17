# FastAPI Application with Posts Data

This FastAPI application serves as a simple API for accessing posts. It provides endpoints to retrieve individual posts, list all posts, create new posts, update existing posts, and delete posts.


# How to Run:

To run this FastAPI application, you need to have Python installed on your system along with the FastAPI library. Follow these steps:

1. Install Python from python.org if you haven't already.

2. Install FastAPI and Uvicorn (ASGI server) using pip:
`pip install fastapi uvicorn`

3. Install FastAPI and Uvicorn (ASGI server) using pip:
`pip install python-dotenv`
   3.1 Create `.env` file in the root of the project use `.env-template` as an example and set your PostgreSQL connection URL   

4. Run the FastAPI application using Uvicorn:
`uvicorn main:app --reload`

5. Once the server starts successfully, you can access the API endpoints from your browser or API testing tools like Postman or curl.
