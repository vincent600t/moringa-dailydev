.PHONY: help install setup db-create db-migrate db-upgrade db-seed db-reset run test test-cov clean lint format

# Variables
PYTHON := python
PIP := pip
FLASK := flask
PYTEST := pytest

help: ## Show this help message
	@echo "Moringa Daily.dev Backend - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	$(PIP) install -r requirements.txt

install-dev: ## Install development dependencies
	$(PIP) install -r requirements.txt
	$(PIP) install pytest-cov black flake8 pylint

setup: install ## Setup the project (install + create .env)
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo ".env file created. Please update it with your configuration."; \
	else \
		echo ".env file already exists."; \
	fi

db-create: ## Create database
	@echo "Creating databases..."
	@echo "Please run the following SQL commands manually:"
	@echo "CREATE DATABASE moringa_dailydev;"
	@echo "CREATE DATABASE moringa_dailydev_test;"
	@echo "CREATE USER moringa_user WITH PASSWORD 'your_password';"
	@echo "GRANT ALL PRIVILEGES ON DATABASE moringa_dailydev TO moringa_user;"
	@echo "GRANT ALL PRIVILEGES ON DATABASE moringa_dailydev_test TO moringa_user;"

db-init: ## Initialize database migrations
	$(FLASK) db init

db-migrate: ## Create a new migration
	$(FLASK) db migrate -m "$(message)"

db-upgrade: ## Apply migrations
	$(FLASK) db upgrade

db-downgrade: ## Rollback last migration
	$(FLASK) db downgrade

db-seed: ## Seed database with sample data
	$(PYTHON) seed_data.py

db-reset: ## Reset database (drop all tables and recreate)
	$(FLASK) db downgrade base
	$(FLASK) db upgrade
	$(PYTHON) seed_data.py

run: ## Run the development server
	$(PYTHON) run.py

run-prod: ## Run with gunicorn (production)
	gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"

test: ## Run tests
	$(PYTEST) tests/ -v

test-cov: ## Run tests with coverage
	$(PYTEST) tests/ -v --cov=app --cov-report=html --cov-report=term

test-watch: ## Run tests in watch mode
	$(PYTEST) tests/ -v --looponfail

test-specific: ## Run specific test file (usage: make test-specific file=test_auth.py)
	$(PYTEST) tests/$(file) -v

clean: ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build

lint: ## Run linting
	flake8 app tests --max-line-length=100 --exclude=migrations

format: ## Format code with black
	black app tests --line-length=100

format-check: ## Check code formatting
	black app tests --check --line-length=100

shell: ## Open Flask shell
	$(FLASK) shell

routes: ## Show all routes
	$(FLASK) routes

create-admin: ## Create admin user (interactive)
	@$(PYTHON) -c "from app import create_app, db; from app.models import User; \
	app = create_app(); \
	with app.app_context(): \
		username = input('Username: '); \
		email = input('Email: '); \
		password = input('Password: '); \
		admin = User(username=username, email=email, password=password, role='admin'); \
		db.session.add(admin); \
		db.session.commit(); \
		print('Admin user created successfully!')"

logs: ## Show application logs
	tail -f app.log

docker-build: ## Build Docker image
	docker build -t moringa-dailydev .

docker-run: ## Run Docker container
	docker run -p 5000:5000 moringa-dailydev

backup-db: ## Backup database
	@echo "Creating database backup..."
	@mkdir -p backups
	@pg_dump -U moringa_user moringa_dailydev > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "Backup created in backups/ directory"

restore-db: ## Restore database from backup (usage: make restore-db file=backup_20240101_120000.sql)
	@echo "Restoring database from $(file)..."
	@psql -U moringa_user moringa_dailydev < backups/$(file)
	@echo "Database restored successfully"

venv: ## Create virtual environment
	$(PYTHON) -m venv venv
	@echo "Virtual environment created. Activate it with:"
	@echo "  source venv/bin/activate  (Linux/Mac)"
	@echo "  venv\\Scripts\\activate  (Windows)"

check: lint test ## Run linting and tests

deploy: ## Deploy to production (placeholder)
	@echo "Deployment steps:"
	@echo "1. Run tests: make test"
	@echo "2. Push to repository"
	@echo "3. SSH to production server"
	@echo "4. Pull latest changes"
	@echo "5. Run migrations: make db-upgrade"
	@echo "6. Restart application server"

status: ## Check application status
	@echo "Checking application status..."
	@curl -s http://localhost:5000/health || echo "Application is not running"

init-project: venv install setup db-init db-migrate db-upgrade db-seed ## Initialize complete project setup
	@echo ""
	@echo "Project initialized successfully!"
	@echo "Next steps:"
	@echo "1. Activate virtual environment: source venv/bin/activate"
	@echo "2. Update .env with your configuration"
	@echo "3. Run the application: make run"