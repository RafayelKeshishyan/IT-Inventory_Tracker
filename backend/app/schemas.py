from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class ItemType(str, Enum):
    device = "device"
    part = "part"


class ItemStatus(str, Enum):
    available = "available"
    in_use = "in_use"
    broken = "broken"
    checked_out = "checked_out"


class ItemBase(BaseModel):
    name: str
    type: ItemType = ItemType.device
    location: Optional[str] = None
    status: ItemStatus = ItemStatus.available
    quantity: int = 1
    low_stock_threshold: int = 5
    notes: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[ItemType] = None
    location: Optional[str] = None
    status: Optional[ItemStatus] = None
    quantity: Optional[int] = None
    low_stock_threshold: Optional[int] = None
    notes: Optional[str] = None


class ItemResponse(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    total_items: int
    total_devices: int
    total_parts: int
    available_count: int
    in_use_count: int
    broken_count: int
    checked_out_count: int
    low_stock_items: list[ItemResponse]
