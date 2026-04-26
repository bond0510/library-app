# app/schemas/borrow_schema.py
from datetime import datetime
from pydantic import BaseModel,ConfigDict

class BorrowCreate(BaseModel):
    member_id: int
    book_id: int

class BorrowResponse(BaseModel):
    id: int
    member_id: int
    book_id: int
    status: str
    issued_at: datetime
    due_date: datetime
    returned_at: datetime | None = None
    fine_amount: float

    model_config = ConfigDict(from_attributes=True)