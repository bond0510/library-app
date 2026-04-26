import logging
from typing import List,Optional

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.borrow_service import BorrowService
from app.schemas.borrow_schema import BorrowCreate, BorrowResponse
from app.schemas.common import PageResponse


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/borrows", tags=["Borrows"])
service = BorrowService()


#  Issue Book
@router.post(
    "",
    response_model=BorrowResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Issue a book",
    description="Issues a book to a member"
)
def borrow_book(req: BorrowCreate, db: Session = Depends(get_db)):
    logger.info(f"Issuing book_id={req.book_id} to member_id={req.member_id}")

    borrow = service.issue_book(db, req.member_id, req.book_id)

    return borrow


#  Return Book
@router.patch(
    "/{borrow_id}/return",
    status_code=status.HTTP_200_OK,
    summary="Return a book"
)
def return_book(borrow_id: int, db: Session = Depends(get_db)):
    logger.info(f"Returning borrow_id={borrow_id}")

    service.return_book(db, borrow_id)

    return {"message": "Book returned successfully"}


#  Get All Borrows (with pagination)
@router.get(
    "",
    response_model=PageResponse[BorrowResponse],
    summary="Get borrows with pagination & filters"
)
def get_borrows(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    member: Optional[str] = Query(None),
    book: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    logger.info(
        f"Fetching borrows skip={skip}, limit={limit}, "
        f"search={search}, member={member}, book={book}, status={status}"
    )
    # convert safely
    member_id = int(member) if member and member.strip() else None
    book_id = int(book) if book and book.strip() else None


    return service.get_all_paginated(
        db, skip, limit, search, member_id, book_id, status
    )


#  Get Borrow by ID
@router.get(
    "/{borrow_id}",
    response_model=BorrowResponse,
    summary="Get borrow by ID"
)
def get_borrow(borrow_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching borrow_id={borrow_id}")

    return service.get_by_id(db, borrow_id)