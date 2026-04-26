from sqlalchemy.orm import Session
from app.models.book import Book
import logging

logger = logging.getLogger(__name__)


class BookRepository:

    def save(self, db: Session, book: Book):
        db.add(book)
        db.commit()
        db.refresh(book)
        logger.info(f"{book.title} Book is created ")
        return book

    def get_by_id(self, db: Session, book_id: int):
        return db.query(Book).filter(Book.id == book_id).first()

    def list_all(self, db: Session):
        return db.query(Book).all()

    def update(self, db: Session, book: Book, data: dict):
        for key, value in data.items():
            setattr(book, key, value)

        db.commit()
        db.refresh(book)
        return book

    def delete(self, db: Session, book: Book):
        db.delete(book)
        db.commit()
    
    def find_by_title_author(self, db: Session, title: str, author: str):
        return (
            db.query(Book)
            .filter(Book.title == title, Book.author == author)
            .first()
        )
    
    def search(self, db: Session, title: str = None, author: str = None, isbn: str = None):
        query = db.query(Book)

        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))

        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))

        if isbn:
            query = query.filter(Book.isbn == isbn)

        return query.all()
    
    def find_all_paginated(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(Book).offset(skip).limit(limit).all()

    def count(self, db: Session):
        return db.query(Book).count() 