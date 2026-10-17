"""
Schemas: Định dạng dữ liệu vào/ra API bằng Pydantic.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


# ============ DISH ============
class DishBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    price: Decimal = Field(..., ge=0)
    category: Optional[str] = Field(None, max_length=50)
    is_available: bool = True


class DishCreate(DishBase):
    """Dùng khi POST /dishes."""
    pass


class DishUpdate(BaseModel):
    """Dùng khi PUT /dishes/{id} — tất cả optional."""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0)
    category: Optional[str] = Field(None, max_length=50)
    is_available: Optional[bool] = None


class DishResponse(DishBase):
    """Dùng khi trả response — có thêm id, created_at."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


# ============ TABLE ============
class TableBase(BaseModel):
    table_number: str = Field(..., max_length=10)
    capacity: int = Field(4, gt=0)
    status: str = Field("available", pattern="^(available|occupied|reserved)$")


class TableCreate(TableBase):
    pass


class TableUpdate(BaseModel):
    table_number: Optional[str] = Field(None, max_length=10)
    capacity: Optional[int] = Field(None, gt=0)
    status: Optional[str] = Field(None, pattern="^(available|occupied|reserved)$")


class TableResponse(TableBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


# ============ ORDER ============
class OrderBase(BaseModel):
    table_id: int
    dish_id: int
    quantity: int = Field(..., gt=0)


class OrderCreate(OrderBase):
    """Dùng khi POST /orders."""
    pass


class OrderUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)
    status: Optional[str] = Field(None, pattern="^(pending|served|paid|cancelled)$")


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    table_id: int
    dish_id: int
    quantity: int
    unit_price: Decimal
    total: Decimal
    status: str
    created_at: datetime