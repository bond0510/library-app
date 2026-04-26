import logging
from sqlalchemy.orm import Session
from app.models.book import Book
from app.repositories.book_repo import BookRepository
from app.core.exceptions import BusinessException
from app.core.error_codes import ErrorCodes

logger = logging.getLogger(__name__)

class BookService:

    def __init__(self):
        self.repo = BookRepository()

    def create_book(self, db: Session, title: str, author: str, total_copies: int,isbn: str):
        if total_copies <= 0:
            raise BusinessException(ErrorCodes.INVALID_BOOK_DATA)

        existing = self.repo.find_by_title_author(db, title, author)

        if existing:
            raise BusinessException(ErrorCodes.BOOK_ALREADY_EXISTS)

        book = Book(
            title=title,
            author=author,
            isbn=isbn,
            total_copies=total_copies,
            available_copies=total_copies
        )

        return self.repo.save(db, book)


    def get_all(self, db: Session):
        books = self.repo.list_all(db)

        if not books:
            raise BusinessException(ErrorCodes.NO_BOOKS_FOUND)

        return books


    def get_by_id(self, db: Session, book_id: int):
        book = self.repo.get_by_id(db, book_id)

        if not book:
            raise BusinessException(ErrorCodes.BOOK_NOT_FOUND)

        return book


    def update_book(self, db: Session, book_id: int, title: str, author: str, total_copies: int,isbn: str):
         book = self.get_by_id(db, book_id)
         data = {
                "title": title,
                "author": author,
                "total_copies": total_copies,
                "isbn": isbn,
                
            }

        # adjust available copies safely
         diff = total_copies - book.total_copies
         book.available_copies += diff

         return self.repo.update(db, book, data)


    def delete_book(self, db: Session, book_id: int):
        book = self.get_by_id(db, book_id)

        self.repo.delete(db, book)
        return {"message": "Book deleted successfully"}


    def is_book_available(self, db: Session, book_id: int):
        book = self.get_by_id(db, book_id)
        return book.available_copies > 0


    def reduce_available_copy(self, db: Session, book_id: int):
        book = self.get_by_id(db, book_id)

        if book.available_copies <= 0:
            raise BusinessException(ErrorCodes.BOOK_NOT_AVAILABLE)

        book.available_copies -= 1
        self.repo.update(db)

        return book


    def increase_available_copy(self, db: Session, book_id: int):
        book = self.get_by_id(db, book_id)

        if book.available_copies >= book.total_copies:
            raise BusinessException(ErrorCodes.BOOK_COPY_LIMIT_EXCEEDED)

        book.available_copies += 1
        self.repo.update(db)

        return book
    
    def search_books(self, db, title=None, author=None, isbn=None):
        results = self.repo.search(db, title, author, isbn)

        if not results:
            raise BusinessException(ErrorCodes.NO_BOOKS_FOUND)

        return results
    
    def get_all_paginated(self, db, skip: int = 0, limit: int = 10):
        books = self.repo.find_all_paginated(db, skip, limit)
        total = self.repo.count(db)
        logger.info(f"Total books count is {total}")
        if not books:
            # optional: return empty instead of exception
            return {
                "data": [],
                "meta": {
                    "total": total,
                    "skip": skip,
                    "limit": limit
                }
            }

        return {
            "data": books,
            "meta": {
                "total": total,
                "skip": skip,
                "limit": limit
            }
        }