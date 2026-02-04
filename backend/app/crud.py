from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional

from . import models, schemas


def get_item(db: Session, item_id: int) -> Optional[models.Item]:
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_items(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    item_type: Optional[str] = None,
    status: Optional[str] = None,
    location: Optional[str] = None,
) -> list[models.Item]:
    query = db.query(models.Item)
    
    if search:
        query = query.filter(
            or_(
                models.Item.name.ilike(f"%{search}%"),
                models.Item.location.ilike(f"%{search}%"),
                models.Item.notes.ilike(f"%{search}%"),
            )
        )
    
    if item_type:
        query = query.filter(models.Item.type == item_type)
    
    if status:
        query = query.filter(models.Item.status == status)
    
    if location:
        query = query.filter(models.Item.location.ilike(f"%{location}%"))
    
    return query.order_by(models.Item.updated_at.desc()).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.ItemCreate) -> models.Item:
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item: schemas.ItemUpdate) -> Optional[models.Item]:
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int) -> bool:
    db_item = get_item(db, item_id)
    if not db_item:
        return False
    
    db.delete(db_item)
    db.commit()
    return True


def get_dashboard_stats(db: Session) -> dict:
    total_items = db.query(models.Item).count()
    total_devices = db.query(models.Item).filter(models.Item.type == "device").count()
    total_parts = db.query(models.Item).filter(models.Item.type == "part").count()
    
    available_count = db.query(models.Item).filter(models.Item.status == "available").count()
    in_use_count = db.query(models.Item).filter(models.Item.status == "in_use").count()
    broken_count = db.query(models.Item).filter(models.Item.status == "broken").count()
    checked_out_count = db.query(models.Item).filter(models.Item.status == "checked_out").count()
    
    # Get items where quantity is below low_stock_threshold (only for parts)
    low_stock_items = db.query(models.Item).filter(
        models.Item.type == "part",
        models.Item.quantity <= models.Item.low_stock_threshold
    ).all()
    
    return {
        "total_items": total_items,
        "total_devices": total_devices,
        "total_parts": total_parts,
        "available_count": available_count,
        "in_use_count": in_use_count,
        "broken_count": broken_count,
        "checked_out_count": checked_out_count,
        "low_stock_items": low_stock_items,
    }


def get_unique_locations(db: Session) -> list[str]:
    """Get all unique locations for filter dropdown"""
    locations = db.query(models.Item.location).distinct().filter(models.Item.location.isnot(None)).all()
    return [loc[0] for loc in locations if loc[0]]
