FROM python:3.9-slim

COPY poetry.lock pyproject.toml /

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root --no-dev

COPY /src /src

EXPOSE 8080

CMD ["streamlit", "run", "src/main.py", "--server.port", "8080"]