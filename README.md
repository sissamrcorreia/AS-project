# 🥗 GoodBite (AS Project)

A web application built with **Django** and **PostgreSQL**, managed via **Docker Compose**.
Use the **Makefile** for all the commands explained below

---

## 🚀 Getting Started

### 1️⃣ Build and start the containers
```bash
docker compose up --build
```
> Builds Docker images (if needed) and starts all services defined in `docker-compose.yml`.

---

## ⚙️ Django Setup

### 2️⃣ Apply database migrations
```bash
docker compose run --rm web python manage.py migrate
```
> Runs Django migrations to create the required database schema.

### 3️⃣ Create a new Django app (example: `agenda`)
```bash
docker compose run --rm web python manage.py startapp agenda
```
> Creates a new Django app named `agenda` inside the `web` container.

### 4️⃣ Create a Django superuser
```bash
docker compose run --rm web python manage.py createsuperuser
```
> Creates an admin user for accessing the Django admin panel (`/admin`).

---

## 🌱 Database Seed (initial demo data)

To load basic demo data (default users, etc.), run:

#### ▶️ Using Docker
```bash
docker compose exec web python manage.py seed
```

This command will create the base demo users:

| Role   | Username      | Password   |
|--------|----------------|------------|
| Admin  | `admin`        | `admin123` |
| Buyer  | `buyer_demo`   | `buyer123` |
| Seller | `seller_demo`  | `seller123` |

> The seed script is located at `GoodBite/management/commands/seed.py`.  
> Modify it later to include demo products, orders, or other data as the project evolves.

---

## 🔐 Roles and Permissions

To create the base user roles and permissions, run:

```bash
docker compose exec web python manage.py setup_roles

---

## 🐘 PostgreSQL Access

### 5️⃣ Connect to the PostgreSQL database
```bash
docker exec -it as-project-db-1 psql -U as_user -d as_db
```
> Opens the PostgreSQL interactive shell inside the database container.

### 6️⃣ List all tables
Once inside the PostgreSQL shell:
```sql
\dt
```
> Displays all tables in the `as_db` database.

---

## 🌐 Accessing the Web App

After the containers are running, open your browser and go to:

👉 [http://localhost:8000](http://localhost:8000)

---

## 🧰 Useful Commands

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

## 👥 Authors
- *Team GoodBite*  
- **Version:** 1.1
