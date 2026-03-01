#!/usr/bin/env python3
"""
OpenClaw Process Monitor - Web Server
Serves the HTML dashboard with real-time data via API endpoints
"""

import json
import asyncio
from pathlib import Path
from monitor import OpenClawMonitor
import http.server
import socketserver
import threading
import time
import urllib.parse

class MonitorHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, monitor_instance=None, **kwargs):
        self.monitor = monitor_instance or OpenClawMonitor()
        super().__init__(*args, **kwargs)
        
    def do_GET(self):
        if self.path == '/api/data':
            self.send_api_response()
        elif self.path == '/api/subagents':
            self.send_subagents_response()
        elif self.path == '/api/processes':
            self.send_processes_response()
        elif self.path == '/api/cron':
            self.send_cron_response()
        elif self.path == '/api/sessions':
            self.send_sessions_response()
        elif self.path.startswith('/api/control/'):
            self.handle_control_request()
        elif self.path == '/' or self.path == '/index.html':
            self.serve_dashboard()
        else:
            super().do_GET()
            
    def do_POST(self):
        if self.path.startswith('/api/control/'):
            self.handle_control_request()
        else:
            self.send_error(404, "Not Found")
            
    def send_api_response(self):
        """Send all monitoring data as JSON"""
        try:
            data = self.monitor.get_all_data()
            self.send_json_response(data)
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
            
    def send_subagents_response(self):
        """Send subagents data"""
        try:
            data = self.monitor.get_subagents()
            self.send_json_response(data)
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
            
    def send_processes_response(self):
        """Send background processes data"""
        try:
            data = self.monitor.get_background_processes()
            self.send_json_response(data)
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
            
    def send_cron_response(self):
        """Send cron jobs data"""
        try:
            data = self.monitor.get_cron_jobs()
            self.send_json_response(data)
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
            
    def send_sessions_response(self):
        """Send active sessions data"""
        try:
            data = self.monitor.get_active_sessions()
            self.send_json_response(data)
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
            
    def handle_control_request(self):
        """Handle control requests for agents/processes"""
        path_parts = self.path.split('/')
        if len(path_parts) < 4:
            self.send_error(400, "Invalid control request")
            return
            
        resource_type = path_parts[3]  # 'subagents' or 'processes'
        action = path_parts[4] if len(path_parts) > 4 else None
        
        if not action:
            self.send_error(400, "No action specified")
            return
            
        # Parse request body for POST requests
        data = {}
        if self.command == 'POST':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                except json.JSONDecodeError:
                    self.send_error(400, "Invalid JSON in request body")
                    return
        
        # Handle different control actions
        result = {'status': 'error', 'message': 'Unknown action'}
        
        if resource_type == 'subagents':
            if action == 'kill' and 'id' in data:
                result = self.kill_subagent(data['id'])
            elif action == 'steer' and 'id' in data and 'message' in data:
                result = self.steer_subagent(data['id'], data['message'])
            elif action == 'logs' and 'id' in data:
                result = self.get_subagent_logs(data['id'])
        elif resource_type == 'processes':
            if action == 'kill' and 'id' in data:
                result = self.kill_process(data['id'])
            elif action == 'logs' and 'id' in data:
                result = self.get_process_logs(data['id'])
                
        self.send_json_response(result)
        
    def kill_subagent(self, agent_id):
        """Kill a subagent"""
        try:
            # In real implementation, would call subagents API
            import subprocess
            result = subprocess.run([
                'openclaw', 'subagents', 'kill', agent_id
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                return {'status': 'success', 'message': f'Subagent {agent_id} killed'}
            else:
                return {'status': 'error', 'message': result.stderr}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
            
    def steer_subagent(self, agent_id, message):
        """Send message to subagent"""
        try:
            # In real implementation, would call subagents steer API
            import subprocess
            result = subprocess.run([
                'openclaw', 'subagents', 'steer', agent_id, message
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                return {'status': 'success', 'message': f'Message sent to {agent_id}'}
            else:
                return {'status': 'error', 'message': result.stderr}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
            
    def get_subagent_logs(self, agent_id):
        """Get logs for a subagent"""
        try:
            # In real implementation, would call appropriate logging API
            return {'status': 'success', 'logs': f'Logs for subagent {agent_id} would appear here'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
            
    def kill_process(self, process_id):
        """Kill a background process"""
        try:
            # In real implementation, would call process kill API
            import subprocess
            result = subprocess.run([
                'openclaw', 'process', 'kill', process_id
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                return {'status': 'success', 'message': f'Process {process_id} killed'}
            else:
                return {'status': 'error', 'message': result.stderr}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
            
    def get_process_logs(self, process_id):
        """Get logs for a background process"""
        try:
            # In real implementation, would call process logs API
            return {'status': 'success', 'logs': f'Logs for process {process_id} would appear here'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
            
    def send_json_response(self, data):
        """Send JSON response with proper headers"""
        json_data = json.dumps(data).encode('utf-8')
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(json_data)))
        self.send_header('Access-Control-Allow-Origin', '*')  # Enable CORS for development
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json_data)
        
    def serve_dashboard(self):
        """Serve the main dashboard HTML with real data injection"""
        try:
            dashboard_path = Path(__file__).parent / 'subagent-monitor.html'
            
            if dashboard_path.exists():
                with open(dashboard_path, 'r') as f:
                    html_content = f.read()
                    
                # Inject real data into the HTML
                real_data = self.monitor.get_all_data()
                
                # Replace mock data with real data
                html_content = html_content.replace(
                    'const mockData = {',
                    f'const mockData = {json.dumps(real_data)}'
                )
                
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', str(len(html_content.encode('utf-8'))))
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
            else:
                self.send_error(404, "Dashboard HTML file not found")
        except Exception as e:
            self.send_error(500, f"Error serving dashboard: {str(e)}")

def create_handler_class(monitor_instance):
    """Create a handler class with monitor instance"""
    class Handler(MonitorHTTPHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, monitor_instance=monitor_instance, **kwargs)
    return Handler

def start_web_server(port=8080):
    """Start the web server"""
    monitor = OpenClawMonitor()
    handler_class = create_handler_class(monitor)
    
    # Change to the dashboard directory so static files are served correctly
    dashboard_dir = Path(__file__).parent
    import os
    os.chdir(dashboard_dir)
    
    with socketserver.TCPServer(("", port), handler_class) as httpd:
        print(f"🚀 OpenClaw Process Monitor Web Server")
        print(f"📊 Dashboard: http://localhost:{port}")
        print(f"🔗 API: http://localhost:{port}/api/data")
        print(f"⏹️  Press Ctrl+C to stop")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='OpenClaw Process Monitor Web Server')
    parser.add_argument('--port', type=int, default=8080, help='Port to serve on (default: 8080)')
    
    args = parser.parse_args()
    start_web_server(args.port)