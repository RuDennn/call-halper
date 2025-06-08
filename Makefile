# Makefile for Django project

# Variables
PYTHON = python
MANAGE = $(PYTHON) manage.py
VENV = venv
PIP = $(VENV)/bin/pip
ENV_FILE = .env

# Default target
all: run

# Install project dependencies
install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Create new migration files
makemigrations:
	$(MANAGE) makemigrations

# Apply migrations to database
migrate:
	$(MANAGE) migrate

# Create superuser
createsuperuser:
	$(MANAGE) createsuperuser

# Run development server
run:
	$(MANAGE) runserver 0.0.0.0:8091

# Run tests
test:
	$(MANAGE) test

# Run production server (example with gunicorn)
prod:
	gunicorn --bind 0.0.0.0:8000 your_project.wsgi:application

# Collect static files
collectstatic:
	$(MANAGE) collectstatic --noinput

# Clean pycache files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

# Format code with black
format:
	black .

# Check code style with flake8
lint:
	flake8 .

# Run security checks
security:
	bandit -r .
	$(MANAGE) check --deploy

# Setup .env file from example
setup-env:
	cp .env.example $(ENV_FILE)

# Full setup (env, install, migrate)
setup: setup-env install migrate

# Show help
help:
	@echo "Available commands:"
	@echo "  make install       - Install project dependencies"
	@echo "  make makemigrations - Create new database migrations"
	@echo "  make migrate       - Apply database migrations"
	@echo "  make createsuperuser - Create admin user"
	@echo "  make run           - Run development server"
	@echo "  make test          - Run tests"
	@echo "  make prod          - Run production server (gunicorn)"
	@echo "  make collectstatic - Collect static files"
	@echo "  make clean         - Clean pycache files"
	@echo "  make format        - Format code with black"
	@echo "  make lint          - Check code style"
	@echo "  make security      - Run security checks"
	@echo "  make setup         - Full project setup"
	@echo "  make help          - Show this help"

.PHONY: all install makemigrations migrate createsuperuser run test prod collectstatic clean format lint security setup help
