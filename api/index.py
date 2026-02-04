import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# Import FastAPI app
from app.main import app

# Use Mangum to wrap FastAPI for serverless
from mangum import Mangum

handler = Mangum(app)
