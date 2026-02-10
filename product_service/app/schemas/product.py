# Define Pydantic Schemas
from pydantic import BaseModel, Field
from typing import List, Optional


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = []


class CategoryResponse(BaseModel):
    id: int
    name: str


class TagResponse(BaseModel):
    id: int
    name: str


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(
        None, gt=0
    )  # Price must be positive if provided # Using Optional fields allows partial updates # gt=0 ensures price > 0
    # category_id: Optional[int] = None
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = []


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    category: Optional[CategoryResponse]
    tags: List[TagResponse] = []


# tag_ids & category_id are sent by clients

# tags & category are returned in responses
