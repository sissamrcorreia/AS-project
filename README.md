# AS Project

A web application built with **Django** and **PostgreSQL**, managed via **Docker Compose**.

---

## Getting Started

### 1. Build and start the containers
```bash
docker compose up --build
```
> Builds Docker images (if needed) and starts all services defined in `docker-compose.yml`.

---

## Django Setup

### 2. Apply database migrations
```bash
docker compose run --rm web python manage.py migrate
```
> Runs Django migrations to create the required database schema.

### 3. Create a new Django app (example: `agenda`)
```bash
docker compose run --rm web python manage.py startapp agenda
```
> Creates a new Django app named `agenda` inside the `web` container.

### 4. Create a Django superuser
```bash
docker compose run --rm web python manage.py createsuperuser
```
> Creates an admin user for accessing the Django admin panel (`/admin`).

---

## PostgreSQL Access

### 5. Connect to the PostgreSQL database
```bash
docker exec -it as-project-db-1 psql -U as_user -d as_db
```
> Opens the PostgreSQL interactive shell inside the database container.

### 6. List all tables
Once inside the PostgreSQL shell:
```sql
\dt
```
> Displays all tables in the `as_db` database.

---

## Accessing the Web App

After the containers are running, open your browser and go to:

[http://localhost:8000](http://localhost:8000)

---

## Useful Commands

Stop all containers:
```bash
docker compose down
```

Check container logs:
```bash
docker compose logs -f
```

Restart only the web service:
```bash
docker compose restart web
```

---

**Authors:** ...  
**Version:** 1.0
