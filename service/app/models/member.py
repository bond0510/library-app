# app/models/member.py
from sqlalchemy import Column, Integer, String,UniqueConstraint
from app.models.base import Base

class Member(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    status = Column(String)

    __table_args__ = (
        UniqueConstraint("email", name="uq_member_email"),
    )