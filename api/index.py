# Vercel Serverless Function for FastAPI
from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# #region agent log
print("[DEBUG] api/index.py loading...")
print(f"[DEBUG] __file__: {__file__}")
print(f"[DEBUG] cwd: {os.getcwd()}")
print(f"[DEBUG] listdir cwd: {os.listdir('.')[:10]}")
# #endregion

# Check if backend exists
backend_path = Path(__file__).parent.parent / "backend"
# #region agent log
print(f"[DEBUG] backend_path: {backend_path}")
print(f"[DEBUG] backend_path exists: {backend_path.exists()}")
if backend_path.exists():
    print(f"[DEBUG] backend contents: {os.listdir(backend_path)}")
# #endregion

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # #region agent log
        print(f"[DEBUG] handler.do_GET called with path: {self.path}")
        # #endregion
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        parsed = urlparse(self.path)
        path = parsed.path
        
        # Simple routing for testing
        if path == '/api/dashboard' or path == '/api/dashboard/':
            response = {
                "total_items": 0,
                "total_devices": 0,
                "total_parts": 0,
                "available_count": 0,
                "in_use_count": 0,
                "broken_count": 0,
                "checked_out_count": 0,
                "low_stock_items": [],
                "debug": "This is a test response - database not connected yet"
            }
        elif path == '/api/items' or path == '/api/items/':
            response = []
        elif path == '/api/locations' or path == '/api/locations/':
            response = []
        else:
            response = {
                "message": "API is working!",
                "path": self.path,
                "note": "Use /api/dashboard, /api/items, or /api/locations"
            }
        
        self.wfile.write(json.dumps(response).encode())
        return
    
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {"message": "POST received", "path": self.path}
        self.wfile.write(json.dumps(response).encode())
        return
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return
