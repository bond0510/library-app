from sqlalchemy.orm import Session
from datetime import datetime,timedelta

from app.models.borrow import Borrow
from app.repositories.borrow_repo import BorrowRepository
from app.services.book_service import BookService
from app.services.member_service import MemberService
from app.core.exceptions import BusinessException
from app.core.error_codes import ErrorCodes


class BorrowService:

    def __init__(self):
        self.repo = BorrowRepository()
        self.book_service = BookService()
        self.member_service = MemberService()

    #  Issue Book
    def issue_book(self, db: Session, member_id: int, book_id: int):
        # Validate member
        member = self.member_service.get_by_id(db, member_id)

        # Validate book
        book = self.book_service.get_by_id(db, book_id)

        # Check availability
        if book.available_copies <= 0:
            raise BusinessException(ErrorCodes.BOOK_NOT_AVAILABLE)

        # Check if already issued (optional rule)
        existing = self.repo.find_active_by_book(db, book_id,member_id)
        if existing:
            raise BusinessException(ErrorCodes.BOOK_ALREADY_ISSUED)

        # Create borrow record
        borrow = Borrow(
            member_id=member.id,
            book_id=book.id,
            status="ISSUED",
            issued_at=datetime.utcnow(),
            due_date=datetime.utcnow() + timedelta(days=14)
        )

        # Reduce available copies
        book.available_copies -= 1

        # Save
        borrow = self.repo.create(db, borrow)

        return borrow


    #  Return Book
    def return_book(self, db: Session, borrow_id: int):
        borrow = self.get_by_id(db, borrow_id)

        if borrow.status == "RETURNED":
            raise BusinessException(ErrorCodes.BORROW_ALREADY_RETURNED)

        now = datetime.utcnow()

        # Calculate fine
        fine = 0
        if now > borrow.due_date:
            delta = now - borrow.due_date
            days_late = math.ceil(delta.total_seconds() / 86400)
            fine = days_late * 10   # ₹10 per day

        borrow.status = "RETURNED"
        borrow.returned_at = now
        borrow.fine_amount = fine
      
        # Increase book copies
        book = self.book_service.get_by_id(db, borrow.book_id)
        book.available_copies += 1

        self.repo.update(db, borrow)

        return borrow

    #  Get by ID
    def get_by_id(self, db: Session, borrow_id: int):
        borrow = self.repo.find_by_id(db, borrow_id)

        if not borrow:
            raise BusinessException(ErrorCodes.BORROW_NOT_FOUND)

        return borrow


    def get_all_paginated(
        self,
        db,
        skip: int,
        limit: int,
        search=None,
        member_id=None,
        book_id=None,
        status=None
    ):
        query = self.repo.base_query(db).filter(Borrow.status == 'ISSUED')

        #  Filters
        if member_id:
            query = query.filter(Borrow.member_id == member_id)

        if book_id:
            query = query.filter(Borrow.book_id == book_id)

        if status:
            query = query.filter(Borrow.status == status)

        #  Search (basic)
        if search:
            query = query.filter(
                (Borrow.status.ilike(f"%{search}%"))
            )

        total = query.count()

        borrows = query.offset(skip).limit(limit).all()

        return {
            "data": borrows,
            "meta": {
                "total": total,
                "skip": skip,
                "limit": limit
            }
        }

    