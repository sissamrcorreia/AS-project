# =========================================================
# 🥗 GoodBite - Makefile
# Simplify common Docker + Django commands
# =========================================================

# =========================================================
# 📦 Setup & Environment
# =========================================================

# Build and start all containers
up:
	docker compose up --build

# Stop all containers
down:
	docker compose down

# Restart only the web service
restart:
	docker compose restart web

# Show container logs (live)
logs:
	docker compose logs -f

# =========================================================
# ⚙️ Django Management
# =========================================================

# Run database migrations
migrate:
	docker compose exec web python manage.py migrate

# Make new migrations (detect model changes)
makemigrations:
	docker compose exec web python manage.py makemigrations

# Create Django superuser
superuser:
	docker compose exec web python manage.py createsuperuser

# Run the Django development server (inside container)
runserver:
	docker compose exec web python manage.py runserver 0.0.0.0:8000

# Open Django shell
shell:
	docker compose exec web python manage.py shell

# =========================================================
# 🌱 Seed & Database
# =========================================================

# Load initial demo data (users, etc.)
seed:
	docker compose exec web python manage.py seed

# Clear all seeded data (users, products, etc.)
clearseed:
	docker compose exec web python manage.py cleardata

# Load base user roles and permissions
roles:
	docker compose exec web python manage.py setup_roles

# Drop and recreate the database (dangerous)
resetdb:
	docker compose exec web python manage.py flush --no-input
	$(MAKE) migrate
	$(MAKE) roles
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
	docker compose ps

# Show database tables
tables:
	$(MAKE) psql CMD="\\dt"

creating:
	$(MAKE) migrate
	$(MAKE) roles
	$(MAKE) seed

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
	@echo "  creating	- Setup database with migrations, roles, and seed data"