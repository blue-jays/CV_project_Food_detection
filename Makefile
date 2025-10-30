.PHONY: help dev build test clean install

help:
	@echo "Snap2Recipe - Available commands:"
	@echo "  make install  - Install all dependencies"
	@echo "  make dev      - Start development servers"
	@echo "  make build    - Build Docker images"
	@echo "  make test     - Run all tests"
	@echo "  make clean    - Clean build artifacts"

install:
	@echo "Installing backend dependencies..."
	cd api && pip install -e .
	@echo "Installing frontend dependencies..."
	cd web && npm install

dev:
	@echo "Starting development environment..."
	docker-compose up

build:
	@echo "Building Docker images..."
	docker-compose build

test:
	@echo "Running backend tests..."
	cd api && pytest tests/ -v
	@echo "Running frontend tests..."
	cd web && npm test

clean:
	@echo "Cleaning build artifacts..."
	docker-compose down -v
	rm -rf api/__pycache__ api/.pytest_cache
	rm -rf web/.next web/node_modules
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
