# 📚 Library App (FastAPI + PostgreSQL + Docker)

A backend service for managing books, members, and borrow operations using **FastAPI**, **SQLAlchemy**, and **PostgreSQL** with Docker support.

---

##  Features

* 📖 Book management (CRUD)
* 👤 Member management
* 🔄 Borrow / Return lifecycle
* ⏱ Overdue tracking + fine calculation
* 📄 Pagination, filtering & search
* 🧾 Structured error handling with traceId
* 🐳 Dockerized setup

---

##  Clone Repository

```bash
git clone https://github.com/bond0510/library-app.git
cd library-app
```

---

##  Setup (Local - Without Docker)

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Environment

**Windows (PowerShell):**

```bash
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run Application

```bash
uvicorn app.main:app --reload
```

---

##  Docker Setup

### Build Docker Image

```bash
docker build -t library-api .
```

---

### Run with Docker Compose

```bash
docker-compose up --build
```

---

##  Service URLs

| Service  | URL                        |
| -------- | -------------------------- |
| FastAPI  | http://localhost:8000      |
| Swagger  | http://localhost:8000/docs |
| Postgres | localhost:5432             |

---

##  Database Configuration

Default credentials (Docker):

```
User: admin
Password: admin123
Database: librarydb
Host: db (inside Docker)
```

---

##  Project Structure

```
app/
 ├── controllers/
 ├── services/
 ├── repositories/
 ├── models/
 ├── schemas/
 ├── core/
 └── main.py
```

---

##  Future Enhancements

*  Authentication & Authorization (JWT)
*  Reporting & analytics
*  Notification system
*  Alembic migrations
*  Cloud deployment (AWS / Kubernetes)

