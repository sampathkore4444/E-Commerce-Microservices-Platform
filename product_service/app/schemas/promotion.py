from pydantic import BaseModel, Field
from typing import Optional, List


class PromotionCreate(BaseModel):
    name: str
    discount_type: str = Field(
        ..., regex="^(percentage|fixed)$", description="Must be 'percentage' or 'fixed'"
    )  # Here elipsis means field Must be 'percentage' or 'fixed' in the request body
    discount_percentage: float = Field(
        ..., gt=0, lt=100, description="Must be between 0 and 100"
    )  # Must be between 0 and 100
    active: bool = True
    product_id: int  #  product_id: list[int] = Field(..., description="List of product IDs this promotion applies to")


class PromotionResponse(BaseModel):
    id: int
    name: str
    discount_type: str
    discount_percentage: float
    active: bool
    product_id: int  # product_ids: List[int] = []


class PromotionUpdate(BaseModel):
    name: Optional[str] = None
    discount_type: Optional[str] = Field(
        None,
        regex="^(percentage|fixed)$",
        description="Must be 'percentage' or 'fixed'",
    )  # why is it optional? Because we want to allow partial updates. If the client only wants to update the name, they shouldn't be forced to provide the discount_type and discount_percentage.
    discount_percentage: Optional[float] = Field(
        None, gt=0, lt=100, description="Must be between 0 and 100"
    )  # why is it optional? Because we want to allow partial updates. If the client only wants to update the name, they shouldn't be forced to provide the discount_type and discount_percentage.
    active: Optional[bool] = None
    product_id: int  # product_ids: List[int] = []
