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

## 🗄️ Database Design

The application uses **PostgreSQL** with the following core entities:

---

###  1. Books Table

Stores book inventory details.

```sql
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(50) UNIQUE,
    total_copies INT NOT NULL,
    available_copies INT NOT NULL,
    
);
```

---

###  2. Members Table

Stores library member information.

```sql
CREATE TABLE members (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    status VARCHAR(20) DEFAULT 'ACTIVE',
    
);
```

---

###  3. Borrows Table

Tracks book issue, return, and overdue lifecycle.

```sql
CREATE TABLE borrows (
    id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    book_id INT NOT NULL,
    status VARCHAR(20) NOT NULL, -- ISSUED, RETURNED, OVERDUE
    issued_at TIMESTAMP,
    due_date TIMESTAMP,
    returned_at TIMESTAMP,
    fine_amount NUMERIC DEFAULT 0,

    CONSTRAINT fk_member FOREIGN KEY (member_id) REFERENCES members(id),
    CONSTRAINT fk_book FOREIGN KEY (book_id) REFERENCES books(id)
);
```

---

##  Entity Relationships

```text
Members (1) ------ (M) Borrows (M) ------ (1) Books
```

* A **Member** can borrow multiple books
* A **Book** can be borrowed multiple times
* `borrows` acts as a junction table with lifecycle tracking

---

##  Borrow Lifecycle

```text
ISSUED → OVERDUE → RETURNED
```

| Status   | Description                |
| -------- | -------------------------- |
| ISSUED   | Book is currently borrowed |
| OVERDUE  | Due date exceeded          |
| RETURNED | Book returned              |

---

##  Fine Calculation Logic

* Fine = ₹10 per day after due date
* Calculated during return

---

##  Indexing (Recommended)

```sql
CREATE INDEX idx_books_title ON books(title);
CREATE INDEX idx_members_email ON members(email);
CREATE INDEX idx_borrows_status ON borrows(status);
```



