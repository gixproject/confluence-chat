FROM python:3.12-slim-bookworm

EXPOSE 8070

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/var/cache/poetry

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN poetry install --without dev --all-extras --no-root

# Copy the application code
COPY . /app

# Run the application
CMD ["streamlit", "run", "confluence_chat/app.py", "--server.address", "0.0.0.0", "--server.port", "8070"]
