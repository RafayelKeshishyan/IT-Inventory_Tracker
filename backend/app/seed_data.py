"""
Seed script to populate the database with sample data for demo/recruiter purposes.
Run this script from the backend directory: python -m app.seed_data
"""

from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import Item, ItemType, ItemStatus

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)


def clear_data(db: Session):
    """Clear all existing data"""
    db.query(Item).delete()
    db.commit()
    print("[OK] Cleared existing data")


def seed_devices(db: Session):
    """Seed device data"""
    devices = [
        # Chromebooks
        Item(
            name="Acer Chromebook 315",
            type=ItemType.device,
            location="Room 205",
            status=ItemStatus.in_use,
            quantity=1,
            notes="Assigned to Ms. Johnson's classroom"
        ),
        Item(
            name="HP Chromebook 14",
            type=ItemType.device,
            location="Room 101",
            status=ItemStatus.available,
            quantity=1,
            notes="Recently cleaned and updated"
        ),
        Item(
            name="Lenovo Chromebook C340",
            type=ItemType.device,
            location="IT Closet",
            status=ItemStatus.broken,
            quantity=1,
            notes="Screen cracked on 1/15/26, warranty claim submitted"
        ),
        Item(
            name="Dell Chromebook 3100",
            type=ItemType.device,
            location="Room 308",
            status=ItemStatus.checked_out,
            quantity=1,
            notes="Checked out to Teacher Smith for remote learning"
        ),
        Item(
            name="Samsung Chromebook 4",
            type=ItemType.device,
            location="Room 412",
            status=ItemStatus.in_use,
            quantity=1,
            notes="Student device for special education"
        ),
        Item(
            name="ASUS Chromebook Flip",
            type=ItemType.device,
            location="Conference Room A",
            status=ItemStatus.available,
            quantity=1,
            notes="Touchscreen model, for presentations"
        ),
        
        # Laptops
        Item(
            name="MacBook Pro 16\" M2",
            type=ItemType.device,
            location="IT Director Office",
            status=ItemStatus.in_use,
            quantity=1,
            notes="IT Director's primary workstation"
        ),
        Item(
            name="Dell Latitude 5420",
            type=ItemType.device,
            location="Conference Room B",
            status=ItemStatus.available,
            quantity=1,
            notes="For guest presentations and video conferencing"
        ),
        Item(
            name="HP EliteBook 840 G8",
            type=ItemType.device,
            location="Room 205",
            status=ItemStatus.in_use,
            quantity=1,
            notes="Teacher's laptop for grading and lesson planning"
        ),
        Item(
            name="Lenovo ThinkPad T14",
            type=ItemType.device,
            location="IT Closet",
            status=ItemStatus.available,
            quantity=1,
            notes="Spare laptop for staff emergencies"
        ),
        Item(
            name="Dell XPS 13",
            type=ItemType.device,
            location="Main Office",
            status=ItemStatus.in_use,
            quantity=1,
            notes="Administrative assistant workstation"
        ),
        Item(
            name="HP ProBook 450",
            type=ItemType.device,
            location="Storage Room",
            status=ItemStatus.broken,
            quantity=1,
            notes="Needs OS reinstall, battery replacement recommended"
        ),
        
        # Other Devices
        Item(
            name="iPad Air 5th Gen",
            type=ItemType.device,
            location="Media Cart",
            status=ItemStatus.in_use,
            quantity=1,
            notes="For video recording and mobile presentations"
        ),
        Item(
            name="Epson Projector EX3280",
            type=ItemType.device,
            location="Auditorium",
            status=ItemStatus.in_use,
            quantity=1,
            notes="Main auditorium projector, serviced 12/2025"
        ),
        Item(
            name="SMART Board Interactive Display 75\"",
            type=ItemType.device,
            location="Room 101",
            status=ItemStatus.in_use,
            quantity=1,
            notes="Installed 09/2025, under warranty until 09/2028"
        ),
        Item(
            name="Canon Printer imageCLASS MF445dw",
            type=ItemType.device,
            location="Teacher Lounge",
            status=ItemStatus.in_use,
            quantity=1,
            notes="Network printer for staff, check toner monthly"
        ),
        Item(
            name="Logitech Webcam C920",
            type=ItemType.device,
            location="Conference Room A",
            status=ItemStatus.available,
            quantity=1,
            notes="For remote meetings and video conferences"
        ),
        Item(
            name="Document Camera IPEVO V4K",
            type=ItemType.device,
            location="Room 308",
            status=ItemStatus.in_use,
            quantity=1,
            notes="Science teacher uses for demonstrations"
        ),
    ]
    
    db.add_all(devices)
    db.commit()
    print(f"[OK] Added {len(devices)} devices")


def seed_parts(db: Session):
    """Seed spare parts data"""
    parts = [
        # LOW STOCK ITEMS (will trigger alerts)
        Item(
            name="Chromebook Chargers (45W USB-C)",
            type=ItemType.part,
            location="IT Closet",
            status=ItemStatus.available,
            quantity=2,
            low_stock_threshold=5,
            notes="URGENT: Need to reorder, only 2 remaining"
        ),
        Item(
            name="USB-C Cables (6ft)",
            type=ItemType.part,
            location="IT Closet",
            status=ItemStatus.available,
            quantity=3,
            low_stock_threshold=8,
            notes="Running low, order more soon"
        ),
        Item(
            name="Wireless Mouse (Logitech M170)",
            type=ItemType.part,
            location="Storage Room",
            status=ItemStatus.available,
            quantity=1,
            low_stock_threshold=5,
            notes="Last one in stock, reorder ASAP"
        ),
        Item(
            name="Laptop Batteries (Dell Compatible)",
            type=ItemType.part,
            location="IT Closet",
            status=ItemStatus.available,
            quantity=3,
            low_stock_threshold=4,
            notes="For Dell Latitude and XPS models"
        ),
        
        # ADEQUATE STOCK ITEMS
        Item(
            name="HDMI Cables (10ft)",
            type=ItemType.part,
            location="IT Closet",
            status=ItemStatus.available,
            quantity=15,
            low_stock_threshold=5,
            notes="Standard HDMI 2.0, good stock level"
        ),
        Item(
            name="Chromebook Keyboard Replacements",
            type=ItemType.part,
            location="Storage Room",
            status=ItemStatus.available,
            quantity=8,
            low_stock_threshold=5,
            notes="Compatible with Acer and HP Chromebooks"
        ),
        Item(
            name="Screen Protectors (11.6\" Chromebook)",
            type=ItemType.part,
            location="IT Closet",
            status=ItemStatus.available,
            quantity=25,
            low_stock_threshold=10,
            notes="Anti-glare, matte finish"
        ),
        Item(
            name="Ethernet Cables Cat6 (25ft)",
            type=ItemType.part,
            location="IT Closet",
            status=ItemStatus.available,
            quantity=20,
            low_stock_threshold=8,
            notes="For wired network connections"
        ),
        Item(
            name="Monitor Stands (Adjustable)",
            type=ItemType.part,
            location="Storage Room",
            status=ItemStatus.available,
            quantity=12,
            low_stock_threshold=5,
            notes="Ergonomic stands for teacher workstations"
        ),
        Item(
            name="USB Hubs (4-Port USB 3.0)",
            type=ItemType.part,
            location="IT Closet",
            status=ItemStatus.available,
            quantity=10,
            low_stock_threshold=4,
            notes="Powered hubs with individual switches"
        ),
        Item(
            name="Laptop Sleeves (13-15\")",
            type=ItemType.part,
            location="Storage Room",
            status=ItemStatus.available,
            quantity=18,
            low_stock_threshold=6,
            notes="Protective cases for device transport"
        ),
        Item(
            name="Cleaning Wipes (Screen Safe)",
            type=ItemType.part,
            location="IT Closet",
            status=ItemStatus.available,
            quantity=8,
            low_stock_threshold=3,
            notes="Alcohol-free, 75 wipes per container"
        ),
        Item(
            name="Stylus Pens (Capacitive)",
            type=ItemType.part,
            location="IT Closet",
            status=ItemStatus.available,
            quantity=14,
            low_stock_threshold=8,
            notes="For touchscreen Chromebooks and tablets"
        ),
    ]
    
    db.add_all(parts)
    db.commit()
    print(f"[OK] Added {len(parts)} spare parts")


def seed_all():
    """Main function to seed all data"""
    db = SessionLocal()
    
    try:
        print("\nStarting database seed...")
        print("=" * 50)
        
        clear_data(db)
        seed_devices(db)
        seed_parts(db)
        
        print("=" * 50)
        print("SUCCESS: Database seeded successfully!")
        print("\nSummary:")
        
        total = db.query(Item).count()
        devices = db.query(Item).filter(Item.type == ItemType.device).count()
        parts = db.query(Item).filter(Item.type == ItemType.part).count()
        low_stock = db.query(Item).filter(
            Item.type == ItemType.part,
            Item.quantity <= Item.low_stock_threshold
        ).count()
        
        print(f"   Total Items: {total}")
        print(f"   Devices: {devices}")
        print(f"   Spare Parts: {parts}")
        print(f"   Low Stock Alerts: {low_stock}")
        print("\nReady to impress recruiters!\n")
        
    except Exception as e:
        print(f"\nERROR: Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_all()
