FROM python:3.13-slim

# Set workdir
WORKDIR /app

# Install poetry
RUN pip install --no-cache-dir poetry

# Copy files
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . .

# Expose port
EXPOSE 8000

# Run the app
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
