CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    isbn VARCHAR(50),
    total_copies INT,
    available_copies INT
);

CREATE TABLE IF NOT EXISTS members (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    status VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS borrows (
    id SERIAL PRIMARY KEY,
    member_id INT,
    book_id INT,
    status VARCHAR(20),
    issued_at TIMESTAMP,
    due_date TIMESTAMP,
    returned_at TIMESTAMP,
    fine_amount NUMERIC
);