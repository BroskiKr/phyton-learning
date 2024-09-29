FROM python:3.9-slim

WORKDIR /my-project

COPY pyproject.toml poetry.lock /my-project/

RUN pip install poetry
RUN poetry install

COPY app /my-project/app
COPY alembic /my-project/alembic
COPY alembic.ini /my-project/
COPY tests /my-project/tests

ENV PYTHONPATH=/my-project

COPY supervisord.conf /etc/supervisor/supervisord.conf

CMD ["sh", "-c","poetry run alembic upgrade head && poetry run supervisord -c /etc/supervisor/supervisord.conf"]
