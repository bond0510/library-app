from sqlalchemy.orm import Session
from app.models.borrow import Borrow


class BorrowRepository:

    #  Create borrow record
    def create(self, db: Session, borrow: Borrow):
        db.add(borrow)
        db.commit()
        db.refresh(borrow)
        return borrow

    #  Find by ID
    def find_by_id(self, db: Session, borrow_id: int):
        return db.query(Borrow).filter(Borrow.id == borrow_id).first()

    #  Get all records
    def find_all(self, db: Session):
        return db.query(Borrow).all()

    #  Pagination
    def find_all_paginated(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(Borrow).offset(skip).limit(limit).all()

    #  Find active borrow (book not returned yet)
    def find_active_by_book(self, db: Session, book_id: int,member_id: int):
        return (
            db.query(Borrow)
            .filter(
                Borrow.book_id == book_id,
                Borrow.member_id == member_id,
                Borrow.status == "ISSUED"
            )
            .first()
        )

    #  Find active borrow by member
    def find_active_by_member(self, db: Session, member_id: int):
        return (
            db.query(Borrow)
            .filter(
                Borrow.member_id == member_id,
                Borrow.status == "ISSUED"
            )
            .all()
        )

    #  Update borrow (status change etc.)
    def update(self, db: Session, borrow: Borrow):
        db.commit()
        db.refresh(borrow)
        return borrow
    
    def base_query(self, db):
        return db.query(Borrow)