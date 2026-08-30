FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry==1.7.1

# Configure poetry to not use virtualenvs inside Docker
RUN poetry config virtualenvs.create false

# Copy dependency files
COPY backend/pyproject.toml backend/poetry.lock* ./backend/

WORKDIR /app/backend

# Install dependencies
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the application
COPY backend/ /app/backend/

# The backend serves the frontend from static/
EXPOSE 8000

CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
