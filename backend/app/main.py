import os
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import engine, get_db, Base
from . import crud, schemas


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IT Inventory Tracker",
    description="Simple inventory management for IT equipment and spare parts",
    version="1.0.0",
)


# CORS setup
# CORS_ORIGINS can still be set in ECS as a comma-separated list.
# The regex below also allows all Vercel production/preview URLs.
default_cors_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://it-inventory-tracker.vercel.app",
    "https://it-inventory-tracker-git-main-rafayelkeshishyan-7187s-projects.vercel.app",
]

extra_cors_origins = os.getenv("CORS_ORIGINS", "").strip()

cors_origins = [
    origin.strip()
    for origin in extra_cors_origins.split(",")
    if origin.strip()
]

allow_origins = list(dict.fromkeys(cors_origins + default_cors_origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "IT Inventory Tracker API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Dashboard endpoint
@app.get("/api/dashboard", response_model=schemas.DashboardStats)
def get_dashboard(db: Session = Depends(get_db)):
    return crud.get_dashboard_stats(db)


# Items endpoints
@app.get("/api/items", response_model=list[schemas.ItemResponse])
def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    type: Optional[str] = None,
    status: Optional[str] = None,
    location: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud.get_items(
        db,
        skip=skip,
        limit=limit,
        search=search,
        item_type=type,
        status=status,
        location=location,
    )


@app.get("/api/items/{item_id}", response_model=schemas.ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/api/items", response_model=schemas.ItemResponse, status_code=201)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)


@app.put("/api/items/{item_id}", response_model=schemas.ItemResponse)
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    updated = crud.update_item(db, item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated


@app.delete("/api/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_item(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}


# Utility endpoints
@app.get("/api/locations", response_model=list[str])
def get_locations(db: Session = Depends(get_db)):
    """Get all unique locations for filter dropdown"""
    return crud.get_unique_locations(db)