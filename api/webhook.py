from http.server import BaseHTTPRequestHandler
import json
import os
from src.bot import process_update
from src.config import SECRET_TOKEN

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle incoming webhook POST requests"""
        request_token = self.headers.get('X-Telegram-Bot-Api-Secret-Token', '')
        
        if SECRET_TOKEN and request_token != SECRET_TOKEN:
            print("Invalid secret token")
            self.send_response(403)
            self.end_headers()
            return
        
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            update = json.loads(body.decode('utf-8'))
            
            print(f"Received update: {update.get('update_id')}")
            
            result = process_update(update)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            print(f"Error in webhook handler: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": str(e)}).encode())
    
    def do_GET(self):
        """Handle GET requests (health check)"""
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Angel Japagenie Bot webhook endpoint is running!')
