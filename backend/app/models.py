from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
import enum

from .database import Base


class ItemType(str, enum.Enum):
    device = "device"
    part = "part"


class ItemStatus(str, enum.Enum):
    available = "available"
    in_use = "in_use"
    broken = "broken"
    checked_out = "checked_out"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    type = Column(Enum(ItemType), nullable=False, default=ItemType.device)
    location = Column(String(100), nullable=True)
    status = Column(Enum(ItemStatus), nullable=False, default=ItemStatus.available)
    quantity = Column(Integer, default=1)
    low_stock_threshold = Column(Integer, default=5)
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
