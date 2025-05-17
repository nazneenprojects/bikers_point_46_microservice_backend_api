.PHONY: install run test build compose-up compose-down

install:
	poetry install

run:
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	poetry run pytest

build:
	docker build -t auth-service:latest .

compose-up:
	docker-compose up --build

compose-down:
	docker-compose down
