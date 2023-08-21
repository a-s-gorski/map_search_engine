FROM python:3.9-slim


COPY poetry.lock pyproject.toml /

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root --no-dev

COPY /app /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]