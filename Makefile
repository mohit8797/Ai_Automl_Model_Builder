.PHONY: help install install-dev run test lint format clean docker docker-up docker-down

help:
	@echo "AutoML Model Builder - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install              Install production dependencies"
	@echo "  make install-dev          Install development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make run                  Run development server"
	@echo "  make test                 Run all tests"
	@echo "  make test-v               Run tests with verbose output"
	@echo "  make test-cov             Run tests with coverage"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint                 Run code linting"
	@echo "  make format               Auto-format code"
	@echo "  make format-check         Check code formatting"
	@echo "  make type-check           Run type checking"
	@echo ""
	@echo "Docker:"
	@echo "  make docker               Build Docker image"
	@echo "  make docker-up            Start Docker Compose services"
	@echo "  make docker-down          Stop Docker Compose services"
	@echo "  make docker-logs          View Docker logs"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean                Clean up temporary files"
	@echo "  make db-init              Initialize database"
	@echo "  make static-files         Process static files"

# Setup targets
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

# Development targets
run:
	python run.py

run-prod:
	gunicorn --bind 0.0.0.0:5000 wsgi:app

run-debug:
	FLASK_ENV=development FLASK_DEBUG=1 python run.py

# Testing targets
test:
	pytest tests/

test-v:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=app --cov=ml --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

test-specific:
	@read -p "Enter test path (e.g., tests/test_validation.py): " test_path; \
	pytest $$test_path -v

# Code quality targets
lint:
	flake8 app/ ml/ --max-line-length=100
	pylint app/ ml/ --disable=all --enable=E,F

lint-fix:
	autopep8 --in-place --aggressive --aggressive -r app/ ml/

format:
	black app/ ml/ tests/
	isort app/ ml/ tests/

format-check:
	black --check app/ ml/ tests/
	isort --check-only app/ ml/ tests/

type-check:
	mypy app/ ml/ --ignore-missing-imports

security-check:
	bandit -r app/ ml/ -ll
	safety check

# Docker targets
docker:
	docker build -t automl-builder:latest .

docker-up:
	docker-compose up -d
	@echo "Services started. Access at http://localhost:5000"

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f web

docker-shell:
	docker-compose exec web /bin/bash

docker-db-shell:
	docker-compose exec db mysql -u automl -p

# Database targets
db-init:
	python -c "from app import create_app; app = create_app(); app.app_context().push()" < database/models.sql

db-clean:
	rm -f *.db *.sqlite

db-shell:
	python

# Utility targets
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage htmlcov/
	rm -rf .pytest_cache/
	rm -rf dist/ build/

clean-uploads:
	rm -rf uploads/datasets/*
	rm -rf outputs/*

clean-logs:
	rm -rf logs/*

clean-all: clean clean-uploads clean-logs db-clean

# Static files
static-files:
	@echo "Static files are in static/ directory"
	@echo "CSS: static/css/style.css"
	@echo "JS: static/js/main.js"

# Documentation
docs:
	cd docs && make html
	@echo "Documentation built. Open docs/_build/html/index.html"

# Development utilities
create-env:
	cp .env.example .env
	@echo "Created .env file. Please edit with your configuration."

create-dirs:
	mkdir -p uploads/datasets
	mkdir -p outputs/models
	mkdir -p outputs/inference
	mkdir -p outputs/reports
	mkdir -p logs

setup-dev: install-dev create-env create-dirs
	@echo "Development environment setup complete!"
	@echo "Run 'make run' to start the development server"

# Performance profiling
profile:
	python -m cProfile -s cumtime run.py

# Dependency checking
check-deps:
	pip outdated
	safety check

update-deps:
	pip list --outdated
	@echo "To update a package: pip install --upgrade <package-name>"

# Git utilities
pre-commit:
	@echo "Running pre-commit checks..."
	make format
	make lint
	make test
	@echo "Pre-commit checks passed!"

# Quick tasks
status:
	@echo "Project Status"
	@echo "=============="
	@echo "Python: $$(python --version)"
	@echo "Flask: $$(pip show flask | grep Version)"
	@echo "TensorFlow: $$(pip show tensorflow | grep Version)"
	@echo ""
	@echo "Directories:"
	@ls -la | grep -E "uploads|outputs|logs|static|templates"

info:
	@echo "AutoML Model Builder"
	@echo "===================="
	@echo "Type 'make help' for available commands"
	@echo ""
	@echo "Quick Start:"
	@echo "  1. make install-dev      # Install all dependencies"
	@echo "  2. make setup-dev        # Create .env and directories"
	@echo "  3. make run              # Start development server"
	@echo "  4. Open http://localhost:5000"
	@echo ""
	@echo "Testing:"
	@echo "  make test                # Run all tests"
	@echo "  make test-cov            # Run tests with coverage"
	@echo ""
	@echo "Code Quality:"
	@echo "  make format              # Auto-format code"
	@echo "  make lint                # Check code quality"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up           # Start with Docker Compose"
	@echo "  make docker-down         # Stop Docker Compose"

.DEFAULT_GOAL := help
