# IT Inventory Tracker

A simple, focused web application for tracking IT equipment and spare parts. Built to solve the real problem of managing Chromebooks, laptops, and supplies across multiple locations.

## 🚀 Quick Demo (For Recruiters)

Want to see the app in action quickly? Follow these steps:

1. **Backend**: `cd backend` → Install deps → `python -m app.seed_data` → `uvicorn app.main:app --reload`
2. **Frontend**: `cd frontend` → `npm install` → `npm run dev`
3. **Visit**: http://localhost:5173

The sample data includes 31 items (18 devices, 13 spare parts) with realistic data including low-stock alerts, multiple locations, and various statuses to showcase all features.

## Features

- **Add/Edit/Delete Items** - Track devices and spare parts with ease
- **Location Tracking** - Know exactly where each item is (Room 101, IT Closet, etc.)
- **Status Management** - Available, In Use, Broken, or Checked Out
- **Search & Filter** - Quickly find items by name, type, location, or status
- **Low Stock Alerts** - Visual warnings when spare parts are running low
- **Clean Dashboard** - At-a-glance overview of your entire inventory

## Tech Stack

- **Frontend**: React + TypeScript + Vite + Tailwind CSS
- **Backend**: FastAPI (Python)
- **Database**: SQLite (no setup required)

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

### Seed Sample Data (Optional)

To populate the database with realistic sample data for demo purposes:

```bash
cd backend
python -m app.seed_data
```

This will add 31 items including:
- 18 devices (Chromebooks, laptops, projectors, iPads, etc.)
- 13 spare parts (chargers, cables, keyboards, etc.)
- 4 low-stock alerts to showcase the alert feature
- Realistic locations, statuses, and notes

Perfect for showcasing the app to recruiters or stakeholders!

**View sample data**: To quickly preview what's in the database:
```bash
python -m app.view_data
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The app will be available at http://localhost:5173

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard` | Get dashboard statistics |
| GET | `/api/items` | List all items (with filtering) |
| GET | `/api/items/{id}` | Get single item |
| POST | `/api/items` | Create new item |
| PUT | `/api/items/{id}` | Update item |
| DELETE | `/api/items/{id}` | Delete item |
| GET | `/api/locations` | Get unique locations |

### Query Parameters for `/api/items`

- `search` - Search by name, location, or notes
- `type` - Filter by type (device/part)
- `status` - Filter by status (available/in_use/broken/checked_out)
- `location` - Filter by location

## Data Model

```
Item:
  - id: number
  - name: string (e.g., "Chromebook", "HDMI Cable")
  - type: "device" | "part"
  - location: string (e.g., "Room 205", "IT Closet")
  - status: "available" | "in_use" | "broken" | "checked_out"
  - quantity: number (for parts)
  - low_stock_threshold: number
  - notes: string
  - created_at: datetime
  - updated_at: datetime
```

## Screenshots

The app features:
- A clean dashboard with status breakdown and low stock alerts
- A searchable/filterable inventory list with card-based display
- A modal form for adding and editing items

## License

MIT
