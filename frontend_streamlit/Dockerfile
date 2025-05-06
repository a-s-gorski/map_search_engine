FROM python:3.9-slim

# Set environment variables to prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends --no-cache-dir \
    build-essential \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

COPY poetry.lock pyproject.toml /
RUN pip install poetry==1.5.1 && poetry config virtualenvs.create false && poetry install --no-root --no-dev

COPY src /src

EXPOSE 8080

CMD ["streamlit", "run", "src/main.py", "--server.port", "8080"]