# app/models/book.py
from sqlalchemy import Column, Integer, String,UniqueConstraint
from app.models.base import Base

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    isbn = Column(String, unique=True, index=True) 
    total_copies = Column(Integer)
    available_copies = Column(Integer)

    __table_args__ = (
        UniqueConstraint("title", "author", name="uq_book_title_author"),
    )