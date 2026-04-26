from sqlalchemy.orm import Session
from app.models.member import Member


class MemberRepository:

    def create(self, db: Session, member: Member):
        db.add(member)
        db.commit()
        db.refresh(member)
        return member

    def find_by_id(self, db: Session, member_id: int):
        return db.query(Member).filter(Member.id == member_id).first()

    def find_all(self, db: Session):
        return db.query(Member).all()

    def find_by_email(self, db: Session, email: str):
        return db.query(Member).filter(Member.email == email).first()

    def update(self, db: Session, member: Member, data: dict):
        for key, value in data.items():
            setattr(member, key, value)
        db.commit()
        db.refresh(member)
        return member

    def delete(self, db: Session, member: Member):
        db.delete(member)
        db.commit()