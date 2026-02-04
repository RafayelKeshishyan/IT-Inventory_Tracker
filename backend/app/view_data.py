"""
Quick utility to view the current database contents.
Run from backend directory: python -m app.view_data
"""

from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Item, ItemType, ItemStatus


def view_all_data():
    """Display all items in the database"""
    db = SessionLocal()
    
    try:
        items = db.query(Item).order_by(Item.type, Item.name).all()
        
        if not items:
            print("\nNo items in database. Run 'python -m app.seed_data' to add sample data.\n")
            return
        
        print("\n" + "=" * 80)
        print("INVENTORY DATABASE CONTENTS")
        print("=" * 80)
        
        # Group by type
        devices = [i for i in items if i.type == ItemType.device]
        parts = [i for i in items if i.type == ItemType.part]
        
        # Display Devices
        print(f"\nDEVICES ({len(devices)}):")
        print("-" * 80)
        for item in devices:
            status_icon = {
                ItemStatus.available: "[AVAIL]",
                ItemStatus.in_use: "[IN USE]",
                ItemStatus.broken: "[BROKEN]",
                ItemStatus.checked_out: "[CHECKOUT]"
            }.get(item.status, "[?]")
            
            location = item.location or "No location"
            print(f"{status_icon} {item.name}")
            print(f"         Location: {location}")
            if item.notes:
                print(f"         Notes: {item.notes}")
            print()
        
        # Display Parts
        print(f"\nSPARE PARTS ({len(parts)}):")
        print("-" * 80)
        for item in parts:
            qty_status = ""
            if item.quantity <= item.low_stock_threshold:
                qty_status = " [LOW STOCK!]"
            
            print(f"{item.name}")
            print(f"         Quantity: {item.quantity} (threshold: {item.low_stock_threshold}){qty_status}")
            print(f"         Location: {item.location}")
            if item.notes:
                print(f"         Notes: {item.notes}")
            print()
        
        # Summary
        print("=" * 80)
        print("SUMMARY:")
        print(f"  Total Items: {len(items)}")
        print(f"  Devices: {len(devices)}")
        print(f"  Spare Parts: {len(parts)}")
        
        available = len([i for i in items if i.status == ItemStatus.available])
        in_use = len([i for i in items if i.status == ItemStatus.in_use])
        broken = len([i for i in items if i.status == ItemStatus.broken])
        checked_out = len([i for i in items if i.status == ItemStatus.checked_out])
        
        print(f"\n  Status Breakdown:")
        print(f"    Available: {available}")
        print(f"    In Use: {in_use}")
        print(f"    Broken: {broken}")
        print(f"    Checked Out: {checked_out}")
        
        low_stock = [i for i in parts if i.quantity <= i.low_stock_threshold]
        print(f"\n  Low Stock Items: {len(low_stock)}")
        if low_stock:
            for item in low_stock:
                print(f"    - {item.name} (only {item.quantity} left)")
        
        print("=" * 80 + "\n")
        
    finally:
        db.close()


if __name__ == "__main__":
    view_all_data()
