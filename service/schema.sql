-- schema.sql

CREATE TABLE members (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    status VARCHAR(20) DEFAULT 'ACTIVE'
);
CREATE UNIQUE INDEX uq_member_email_lower ON members (LOWER(email));

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    author VARCHAR(100),
    isbn VARCHAR(20) UNIQUE,
    total_copies INT,
    available_copies INT
);

CREATE TABLE borrows (
    id SERIAL PRIMARY KEY,
    book_id INT REFERENCES books(id),
    member_id INT REFERENCES members(id),
    issue_date DATE,
    due_date DATE,
    return_date DATE,
    status VARCHAR(20)
);