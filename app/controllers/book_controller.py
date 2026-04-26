from fastapi import APIRouter, Depends, status,Query
from sqlalchemy.orm import Session
from typing import List,Optional

from app.db import get_db
from app.services.book_service import BookService
from app.schemas.book_schema import BookCreate, BookUpdate, BookResponse

router = APIRouter(prefix="/books", tags=["Books"])
service = BookService()


#  Create Book
@router.post(
    "",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new book"
)
def create_book(req: BookCreate, db: Session = Depends(get_db)):
    return service.create_book(
        db,
        title=req.title,
        author=req.author,
        isbn=req.isbn,
        total_copies=req.total_copies
    )


#  Get All Books
@router.get(
    "",
    response_model=List[BookResponse],
    summary="Get all books"
)
def get_all_books(db: Session = Depends(get_db)):
    return service.get_all(db)

#Search book
@router.get("/search", 
            response_model=List[BookResponse], 
            summary="Search books")
def search_books(
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    isbn: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return service.search_books(db, title, author, isbn)

@router.get("/paginated", summary="Get books with pagination")
def get_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    return service.get_all_paginated(db, skip, limit)

#  Get Book by ID
@router.get(
    "/{book_id}",
    response_model=BookResponse,
    summary="Get book by ID"
)
def get_book(book_id: int, db: Session = Depends(get_db)):
    return service.get_by_id(db, book_id)


#  Update Book
@router.put(
    "/{book_id}",
    response_model=BookResponse,
    summary="Update book details"
)
def update_book(book_id: int, req: BookUpdate, db: Session = Depends(get_db)):
    return service.update_book(
        db,
        book_id=book_id,
        title=req.title,
        author=req.author,
        isbn=req.isbn,
        total_copies=req.total_copies
    )

# Delete Book
@router.delete(
    "/{book_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a book"
)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return service.delete_book(db, book_id)


#  Check Availability
@router.get(
    "/{book_id}/availability",
    summary="Check book availability"
)
def check_availability(book_id: int, db: Session = Depends(get_db)):
    available = service.is_book_available(db, book_id)
    return {"available": available}

