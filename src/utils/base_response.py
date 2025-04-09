from typing import Generic, Optional, TypeVar, List, Any
from pydantic import BaseModel
from pydantic.generics import GenericModel


T = TypeVar("T")

class SuccessResponse(GenericModel, Generic[T]):
    status: bool = True
    status_code: int
    message: str
    data: Optional[T] = None

class FailureResponse(GenericModel):
    status: bool = False
    status_code: int
    message: str

class PaginationMeta(BaseModel):
    total: int
    page: int
    size: int
    pages: int

class PaginatedResponse(GenericModel, Generic[T]):
    status: bool = True
    status_code: int
    message: str
    data: List[T]
    meta: PaginationMeta
