# Vercel Serverless Function for IT Inventory Tracker API
from http.server import BaseHTTPRequestHandler
import json
import os
import re
from urllib.parse import parse_qs, urlparse
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """Get database connection using Neon PostgreSQL URL"""
    database_url = os.environ.get('DATABASE_URL_UNPOOLED') or os.environ.get('POSTGRES_URL')
    if not database_url:
        raise Exception("No database URL found in environment variables")
    
    # Handle postgres:// vs postgresql:// prefix
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    return psycopg2.connect(database_url, cursor_factory=RealDictCursor)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

class handler(BaseHTTPRequestHandler):
    def send_json_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, default=json_serial).encode())
    
    def send_error_response(self, status_code, message):
        self.send_json_response(status_code, {"detail": message})
    
    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            path = parsed.path.rstrip('/')
            query_params = parse_qs(parsed.query)
            
            # GET /api/dashboard
            if path == '/api/dashboard':
                self.handle_dashboard()
            # GET /api/items
            elif path == '/api/items':
                self.handle_get_items(query_params)
            # GET /api/items/{id}
            elif re.match(r'^/api/items/\d+$', path):
                item_id = int(path.split('/')[-1])
                self.handle_get_item(item_id)
            # GET /api/locations
            elif path == '/api/locations':
                self.handle_get_locations()
            # Root API
            elif path == '/api' or path == '':
                self.send_json_response(200, {"message": "IT Inventory Tracker API", "version": "1.0.0"})
            else:
                self.send_error_response(404, f"Not found: {path}")
        except Exception as e:
            self.send_error_response(500, str(e))
    
    def do_POST(self):
        try:
            parsed = urlparse(self.path)
            path = parsed.path.rstrip('/')
            
            # POST /api/items
            if path == '/api/items':
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                data = json.loads(body) if body else {}
                self.handle_create_item(data)
            else:
                self.send_error_response(404, f"Not found: {path}")
        except json.JSONDecodeError:
            self.send_error_response(400, "Invalid JSON")
        except Exception as e:
            self.send_error_response(500, str(e))
    
    def do_PUT(self):
        try:
            parsed = urlparse(self.path)
            path = parsed.path.rstrip('/')
            
            # PUT /api/items/{id}
            if re.match(r'^/api/items/\d+$', path):
                item_id = int(path.split('/')[-1])
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                data = json.loads(body) if body else {}
                self.handle_update_item(item_id, data)
            else:
                self.send_error_response(404, f"Not found: {path}")
        except json.JSONDecodeError:
            self.send_error_response(400, "Invalid JSON")
        except Exception as e:
            self.send_error_response(500, str(e))
    
    def do_DELETE(self):
        try:
            parsed = urlparse(self.path)
            path = parsed.path.rstrip('/')
            
            # DELETE /api/items/{id}
            if re.match(r'^/api/items/\d+$', path):
                item_id = int(path.split('/')[-1])
                self.handle_delete_item(item_id)
            else:
                self.send_error_response(404, f"Not found: {path}")
        except Exception as e:
            self.send_error_response(500, str(e))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    # === Handler Methods ===
    
    def handle_dashboard(self):
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            
            # Get counts
            cur.execute("SELECT COUNT(*) as count FROM items")
            total_items = cur.fetchone()['count']
            
            cur.execute("SELECT COUNT(*) as count FROM items WHERE type = 'device'")
            total_devices = cur.fetchone()['count']
            
            cur.execute("SELECT COUNT(*) as count FROM items WHERE type = 'part'")
            total_parts = cur.fetchone()['count']
            
            cur.execute("SELECT COUNT(*) as count FROM items WHERE status = 'available'")
            available_count = cur.fetchone()['count']
            
            cur.execute("SELECT COUNT(*) as count FROM items WHERE status = 'in_use'")
            in_use_count = cur.fetchone()['count']
            
            cur.execute("SELECT COUNT(*) as count FROM items WHERE status = 'broken'")
            broken_count = cur.fetchone()['count']
            
            cur.execute("SELECT COUNT(*) as count FROM items WHERE status = 'checked_out'")
            checked_out_count = cur.fetchone()['count']
            
            # Get low stock items
            cur.execute("""
                SELECT * FROM items 
                WHERE type = 'part' AND quantity <= low_stock_threshold
            """)
            low_stock_items = [dict(row) for row in cur.fetchall()]
            
            response = {
                "total_items": total_items,
                "total_devices": total_devices,
                "total_parts": total_parts,
                "available_count": available_count,
                "in_use_count": in_use_count,
                "broken_count": broken_count,
                "checked_out_count": checked_out_count,
                "low_stock_items": low_stock_items
            }
            self.send_json_response(200, response)
        finally:
            conn.close()
    
    def handle_get_items(self, query_params):
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            
            # Build query with filters
            query = "SELECT * FROM items WHERE 1=1"
            params = []
            
            search = query_params.get('search', [None])[0]
            if search:
                query += " AND (name ILIKE %s OR location ILIKE %s OR notes ILIKE %s)"
                search_pattern = f"%{search}%"
                params.extend([search_pattern, search_pattern, search_pattern])
            
            item_type = query_params.get('type', [None])[0]
            if item_type:
                query += " AND type = %s"
                params.append(item_type)
            
            status = query_params.get('status', [None])[0]
            if status:
                query += " AND status = %s"
                params.append(status)
            
            location = query_params.get('location', [None])[0]
            if location:
                query += " AND location ILIKE %s"
                params.append(f"%{location}%")
            
            query += " ORDER BY updated_at DESC"
            
            cur.execute(query, params)
            items = [dict(row) for row in cur.fetchall()]
            
            self.send_json_response(200, items)
        finally:
            conn.close()
    
    def handle_get_item(self, item_id):
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM items WHERE id = %s", (item_id,))
            item = cur.fetchone()
            
            if item:
                self.send_json_response(200, dict(item))
            else:
                self.send_error_response(404, "Item not found")
        finally:
            conn.close()
    
    def handle_get_locations(self):
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT location FROM items WHERE location IS NOT NULL AND location != '' ORDER BY location")
            locations = [row['location'] for row in cur.fetchall()]
            self.send_json_response(200, locations)
        finally:
            conn.close()
    
    def handle_create_item(self, data):
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            
            cur.execute("""
                INSERT INTO items (name, type, location, status, quantity, low_stock_threshold, notes, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                RETURNING *
            """, (
                data.get('name'),
                data.get('type', 'device'),
                data.get('location', ''),
                data.get('status', 'available'),
                data.get('quantity', 1),
                data.get('low_stock_threshold', 5),
                data.get('notes', '')
            ))
            
            item = cur.fetchone()
            conn.commit()
            
            self.send_json_response(201, dict(item))
        finally:
            conn.close()
    
    def handle_update_item(self, item_id, data):
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            
            # Check if item exists
            cur.execute("SELECT * FROM items WHERE id = %s", (item_id,))
            existing = cur.fetchone()
            if not existing:
                self.send_error_response(404, "Item not found")
                return
            
            # Update item
            cur.execute("""
                UPDATE items SET
                    name = COALESCE(%s, name),
                    type = COALESCE(%s, type),
                    location = COALESCE(%s, location),
                    status = COALESCE(%s, status),
                    quantity = COALESCE(%s, quantity),
                    low_stock_threshold = COALESCE(%s, low_stock_threshold),
                    notes = COALESCE(%s, notes),
                    updated_at = NOW()
                WHERE id = %s
                RETURNING *
            """, (
                data.get('name'),
                data.get('type'),
                data.get('location'),
                data.get('status'),
                data.get('quantity'),
                data.get('low_stock_threshold'),
                data.get('notes'),
                item_id
            ))
            
            item = cur.fetchone()
            conn.commit()
            
            self.send_json_response(200, dict(item))
        finally:
            conn.close()
    
    def handle_delete_item(self, item_id):
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            
            # Check if item exists
            cur.execute("SELECT * FROM items WHERE id = %s", (item_id,))
            existing = cur.fetchone()
            if not existing:
                self.send_error_response(404, "Item not found")
                return
            
            cur.execute("DELETE FROM items WHERE id = %s", (item_id,))
            conn.commit()
            
            self.send_json_response(200, {"message": "Item deleted successfully"})
        finally:
            conn.close()
