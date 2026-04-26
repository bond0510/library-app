from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from app.models.base import Base


class Borrow(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, nullable=False)
    book_id = Column(Integer, nullable=False)

    status = Column(String, nullable=False)  # ISSUED / OVERDUE / RETURNED

    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    due_date = Column(DateTime, nullable=False)
    returned_at = Column(DateTime, nullable=True)

    fine_amount = Column(Float, default=0.0)