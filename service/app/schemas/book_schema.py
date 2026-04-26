from pydantic import BaseModel, Field,ConfigDict
from typing import Optional


#  Base (shared fields)
class BookBase(BaseModel):
    title: str = Field(..., example="Clean Code", description="Book title", )
    author: str = Field(..., example="Robert C. Martin", description="Author name")
    isbn: str = Field(..., example="978-0-306-40615-7", description="The International Standard Book Number")


# Create request
class BookCreate(BookBase):
    total_copies: int = Field(..., gt=0, example=5, description="Total copies of the book")


# Update request (full update)
class BookUpdate(BookBase):
    total_copies: int = Field(..., gt=0)


# Partial update (PATCH)
class BookPatch(BaseModel):
    title: Optional[str] = Field(None, example="Clean Architecture")
    author: Optional[str] = Field(None, example="Robert C. Martin")
    total_copies: Optional[int] = Field(None, gt=0)


# Response model
class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    total_copies: int
    available_copies: int

    model_config = ConfigDict(from_attributes=True)