# =========================================================
# 🥗 GoodBite - Makefile
# Simplify common Docker + Django commands
# =========================================================

# Variables
DOCKER_COMPOSE = docker compose
WEB_SERVICE = web

# =========================================================
# 📦 Setup & Environment
# =========================================================

# Build and start all containers
up:
	$(DOCKER_COMPOSE) up --build

# Stop all containers
down:
	$(DOCKER_COMPOSE) down

# Restart only the web service
restart:
	$(DOCKER_COMPOSE) restart $(WEB_SERVICE)

# Show container logs (live)
logs:
	$(DOCKER_COMPOSE) logs -f

# =========================================================
# ⚙️ Django Management
# =========================================================

# Run database migrations
migrate:
	$(DOCKER_COMPOSE) exec $(WEB_SERVICE) python manage.py migrate

# Make new migrations (detect model changes)
makemigrations:
	$(DOCKER_COMPOSE) exec $(WEB_SERVICE) python manage.py makemigrations

# Create Django superuser
superuser:
	$(DOCKER_COMPOSE) exec $(WEB_SERVICE) python manage.py createsuperuser

# Run the Django development server (inside container)
runserver:
	$(DOCKER_COMPOSE) exec $(WEB_SERVICE) python manage.py runserver 0.0.0.0:8000

# Open Django shell
shell:
	$(DOCKER_COMPOSE) exec $(WEB_SERVICE) python manage.py shell

# =========================================================
# 🌱 Seed & Database
# =========================================================

# Load initial demo data (users, etc.)
seed:
	$(DOCKER_COMPOSE) exec $(WEB_SERVICE) python manage.py seed

# Drop and recreate the database (dangerous)
resetdb:
	$(DOCKER_COMPOSE) exec $(WEB_SERVICE) python manage.py flush --no-input
	$(MAKE) migrate
	$(MAKE) seed

# Access PostgreSQL shell
psql:
	docker exec -it as-project-db-1 psql -U as_user -d as_db

# =========================================================
# 🧹 Utilities
# =========================================================

# Clean up unused Docker resources
clean:
	docker system prune -f

# List running containers
ps:
	$(DOCKER_COMPOSE) ps

# Show database tables
tables:
	$(MAKE) psql CMD="\\dt"

# =========================================================
# Default target
# =========================================================
help:
	@echo "Available commands:"
	@echo "  up          - Build and start all containers"
	@echo "  down        - Stop all containers"
	@echo "  restart     - Restart web container"
	@echo "  logs        - Show logs"
	@echo "  migrate     - Apply database migrations"
	@echo "  makemigrations - Create new migrations"
	@echo "  superuser   - Create Django superuser"
	@echo "  runserver   - Run Django dev server"
	@echo "  shell       - Open Django shell"
	@echo "  seed        - Load demo data"
	@echo "  resetdb     - Reset and reseed the DB"
	@echo "  psql        - Open PostgreSQL shell"
	@echo "  clean       - Remove unused Docker resources"
	@echo "  ps          - Show running containers"
	@echo "  tables      - List database tables"