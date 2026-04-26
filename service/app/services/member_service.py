from sqlalchemy.orm import Session
from app.models.member import Member
from app.repositories.member_repo import MemberRepository
from app.core.exceptions import BusinessException
from app.core.error_codes import ErrorCodes


class MemberService:

    def __init__(self):
        self.repo = MemberRepository()

    def create_member(self, db: Session, name: str, email: str, phone: str):
        existing = self.repo.find_by_email(db, email)
        if existing:
            raise BusinessException(ErrorCodes.MEMBER_ALREADY_EXISTS)

        member = Member(
            name=name,
            email=email,
            phone=phone,
            status="ACTIVE"
        )

        return self.repo.create(db, member)

    def get_all(self, db: Session):
        members = self.repo.find_all(db)

        if not members:
            raise BusinessException(ErrorCodes.NO_MEMBERS_FOUND)

        return members

    def get_by_id(self, db: Session, member_id: int):
        member = self.repo.find_by_id(db, member_id)

        if not member:
            raise BusinessException(ErrorCodes.MEMBER_NOT_FOUND)

        return member

    def update_member(self, db: Session, member_id: int, data: dict):
        member = self.get_by_id(db, member_id)
        return self.repo.update(db, member, data)

    def delete_member(self, db: Session, member_id: int):
        member = self.get_by_id(db, member_id)
        self.repo.delete(db, member)
        return {"message": "Member deleted successfully"}