from typing import Generic, TypeVar, List
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class PageMeta(BaseModel):
    total: int
    skip: int
    limit: int


class PageResponse(BaseModel, Generic[T]):
    data: List[T]
    meta: PageMeta

    model_config = ConfigDict(from_attributes=True)