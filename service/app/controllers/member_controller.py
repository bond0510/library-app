from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.services.member_service import MemberService
from app.schemas.member_schema import MemberCreate, MemberUpdate, MemberResponse

router = APIRouter(prefix="/members", tags=["Members"])
service = MemberService()


#  Create Member
@router.post("", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def create_member(req: MemberCreate, db: Session = Depends(get_db)):
    return service.create_member(db, req.name, req.email, req.phone)


#  Get All Members
@router.get("", response_model=List[MemberResponse])
def get_members(db: Session = Depends(get_db)):
    return service.get_all(db)


#  Get Member by ID
@router.get("/{member_id}", response_model=MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):
    return service.get_by_id(db, member_id)


#  Update Member
@router.patch("/{member_id}", response_model=MemberResponse)
def update_member(member_id: int, req: MemberUpdate, db: Session = Depends(get_db)):
    return service.update_member(member_id=member_id, db=db, data=req.dict(exclude_unset=True))


#  Delete Member
@router.delete("/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    return service.delete_member(db, member_id)