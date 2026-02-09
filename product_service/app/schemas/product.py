# Define Pydantic Schemas
from pydantic import BaseModel, Field
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)  # Price must be positive if provided


# Using Optional fields allows partial updates
# gt=0 ensures price > 0
