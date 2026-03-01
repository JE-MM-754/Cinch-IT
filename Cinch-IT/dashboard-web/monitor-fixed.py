#!/usr/bin/env python3
"""
OpenClaw Process Monitor - Fixed Version
Real-time dashboard for tracking subagents, processes, and system status
"""

import json
import subprocess
import time
import datetime
from pathlib import Path
import sys
import os

class OpenClawMonitor:
    def __init__(self):
        self.workspace = Path.home() / ".openclaw" / "workspace"
        
    def get_background_processes(self):
        """Get background processes from process list"""
        try:
            # Use the process tool directly via OpenClaw
            result = subprocess.run([
                'openclaw', 'process', 'list'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                processes = []
                lines = result.stdout.strip().split('\n')
                
                for line in lines:
                    if 'running' in line or 'stopped' in line:
                        parts = line.split()
                        if len(parts) >= 4:
                            session_id = parts[0] if parts else 'unknown'
                            status = parts[1] if len(parts) > 1 else 'unknown'  
                            runtime = parts[2] if len(parts) > 2 else 'unknown'
                            command = ' '.join(parts[4:]) if len(parts) > 4 else 'Unknown Command'
                            
                            processes.append({
                                'id': session_id,
                                'name': command[:50] + '...' if len(command) > 50 else command,
                                'status': status,
                                'runtime': runtime,
                                'key': session_id,
                                'tokens': 'N/A'
                            })
                return processes
        except Exception as e:
            print(f"Error fetching background processes: {e}")
            
        return []
        
    def get_active_sessions(self):
        """Get all active OpenClaw sessions"""
        try:
            result = subprocess.run([
                'openclaw', 'sessions', 'list', '--json'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                sessions_data = json.loads(result.stdout)
                sessions = []
                for session in sessions_data.get('sessions', []):
                    age_ms = session.get('updatedAt', 0)
                    age = self._calculate_runtime(age_ms) if age_ms else 'unknown'
                    
                    sessions.append({
                        'key': session.get('key', 'unknown'),
                        'channel': session.get('channel', 'unknown'),
                        'age': age,
                        'tokens': f"{session.get('totalTokens', 0)}/{session.get('contextTokens', 0)}",
                        'model': session.get('model', 'unknown').split('/')[-1] if session.get('model') else 'unknown'
                    })
                return sessions
        except Exception as e:
            print(f"Error fetching active sessions: {e}")
            
        return []
        
    def get_subagents(self):
        """Get active and recent subagents"""
        try:
            result = subprocess.run([
                'openclaw', 'subagents', 'list'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                subagents = []
                
                # Parse the text output for subagents
                lines = result.stdout.split('\n')
                in_active = False
                in_recent = False
                
                for line in lines:
                    if 'active subagents:' in line:
                        in_active = True
                        in_recent = False
                        continue
                    elif 'recent (last' in line:
                        in_active = False  
                        in_recent = True
                        continue
                    elif line.startswith('(none)'):
                        continue
                    elif line.strip() and (in_active or in_recent):
                        # Parse lines like: "1. Gaming Research Agent (claude-sonnet-4-20250514, 3m, tokens 10k...) done - Research HD2..."
                        if '. ' in line:
                            parts = line.strip().split('. ', 1)
                            if len(parts) > 1:
                                details = parts[1]
                                
                                # Extract name (everything before first parenthesis)
                                name_end = details.find('(')
                                name = details[:name_end].strip() if name_end > 0 else details.split()[0]
                                
                                # Extract status and runtime from the line
                                status = 'running' if in_active else 'completed'
                                if 'done' in line:
                                    status = 'completed'
                                elif 'running' in line:
                                    status = 'running'
                                
                                # Extract runtime (look for patterns like "3m", "1h 30m")
                                runtime = 'unknown'
                                if '(' in details and ')' in details:
                                    paren_content = details[details.find('(')+1:details.find(')')]
                                    parts = paren_content.split(',')
                                    for part in parts:
                                        part = part.strip()
                                        if any(x in part for x in ['m', 'h', 's']) and 'claude' not in part:
                                            runtime = part
                                            break
                                
                                # Extract model
                                model = 'claude-sonnet-4-20250514'  # default
                                if 'claude-sonnet' in details:
                                    model_start = details.find('claude-sonnet')
                                    model_end = details.find(',', model_start)
                                    if model_end > model_start:
                                        model = details[model_start:model_end].strip()
                                
                                # Extract task description
                                task = details
                                if ' - ' in details:
                                    task = details.split(' - ', 1)[1]
                                task = task[:100] + '...' if len(task) > 100 else task
                                
                                subagents.append({
                                    'id': name.lower().replace(' ', '-'),
                                    'name': name,
                                    'status': status,
                                    'runtime': runtime,
                                    'model': model,
                                    'task': task,
                                    'tokens': 'N/A'
                                })
                
                return subagents
        except Exception as e:
            print(f"Error fetching subagents: {e}")
            
        return []
        
    def get_cron_jobs(self):
        """Get scheduled cron jobs"""
        try:
            result = subprocess.run([
                'openclaw', 'cron', 'list'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                jobs = []
                lines = result.stdout.strip().split('\n')
                
                # Skip header line
                for line in lines[1:]:
                    if line.strip() and not line.startswith('ID'):
                        parts = line.split(None, 6)  # Split on whitespace, max 7 parts
                        if len(parts) >= 4:
                            # Format: ID NAME SCHEDULE NEXT LAST STATUS TARGET AGENT
                            jobs.append({
                                'name': parts[1] if len(parts) > 1 else 'Unnamed Job',
                                'schedule': parts[2] if len(parts) > 2 else 'unknown',
                                'nextRun': parts[3] if len(parts) > 3 else 'unknown',
                                'status': parts[5] if len(parts) > 5 else 'unknown',
                                'id': parts[0] if len(parts) > 0 else 'unknown'
                            })
                return jobs
        except Exception as e:
            print(f"Error fetching cron jobs: {e}")
            
        return []
        
    def _calculate_runtime(self, timestamp_ms):
        """Calculate runtime from timestamp"""
        if not timestamp_ms:
            return "unknown"
            
        try:
            start_time = datetime.datetime.fromtimestamp(timestamp_ms / 1000)
            now = datetime.datetime.now()
            delta = now - start_time
            return self._format_time_delta(delta)
        except:
            return "unknown"
            
    def _format_time_delta(self, delta):
        """Format time delta as human readable string"""
        total_seconds = int(delta.total_seconds())
        
        if total_seconds < 0:
            return "future"
            
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m"
        else:
            return f"{seconds}s"
            
    def get_all_data(self):
        """Get all monitoring data"""
        return {
            'timestamp': datetime.datetime.now().isoformat(),
            'subagents': self.get_subagents(),
            'processes': self.get_background_processes(),
            'cronJobs': self.get_cron_jobs(),
            'sessions': self.get_active_sessions()
        }
        
    def print_terminal_dashboard(self):
        """Print a terminal-based dashboard"""
        data = self.get_all_data()
        
        # Clear screen
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("=" * 80)
        print("🚀 OPENCLAW PROCESS MONITOR".center(80))
        print("=" * 80)
        print(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Stats summary
        print(f"\n📊 OVERVIEW:")
        print(f"  Active Subagents:     {len(data['subagents'])}")
        print(f"  Background Processes: {len(data['processes'])}")
        print(f"  Scheduled Jobs:       {len(data['cronJobs'])}")
        print(f"  Active Sessions:      {len(data['sessions'])}")
        
        # Subagents
        print(f"\n🤖 ACTIVE SUBAGENTS ({len(data['subagents'])}):")
        if data['subagents']:
            for agent in data['subagents']:
                status_icon = "🟢" if agent['status'] == 'running' else "🔴" if agent['status'] == 'completed' else "⏸️"
                print(f"  {status_icon} {agent['name']}")
                print(f"     Status: {agent['status']} | Runtime: {agent['runtime']}")
                print(f"     Model: {agent['model']}")
                print(f"     Task: {agent['task']}")
        else:
            print("  No subagents found")
            
        # Background Processes
        print(f"\n⚙️ BACKGROUND PROCESSES ({len(data['processes'])}):")
        if data['processes']:
            for proc in data['processes']:
                status_icon = "🟢" if proc['status'] == 'running' else "🔴"
                print(f"  {status_icon} {proc['name']}")
                print(f"     Status: {proc['status']} | Runtime: {proc['runtime']}")
                print(f"     Session: {proc['key']}")
        else:
            print("  No background processes running")
            
        # Cron Jobs
        print(f"\n⏰ SCHEDULED JOBS ({len(data['cronJobs'])}):")
        if data['cronJobs']:
            for job in data['cronJobs']:
                status_icon = "🟢" if job['status'] in ['ok', 'idle'] else "⚠️" if job['status'] == 'error' else "⏸️"
                print(f"  {status_icon} {job['name']}")
                print(f"     Schedule: {job['schedule']} | Next: {job['nextRun']}")
                print(f"     Status: {job['status']}")
        else:
            print("  No scheduled jobs found")
            
        # Active Sessions
        print(f"\n📊 ACTIVE SESSIONS ({len(data['sessions'])}):")
        if data['sessions']:
            for session in data['sessions']:
                print(f"  🔗 {session['channel']} ({session['age']})")
                print(f"     Tokens: {session['tokens']} | Model: {session['model']}")
        else:
            print("  No active sessions")
            
        print("\n" + "=" * 80)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='OpenClaw Process Monitor')
    parser.add_argument('--mode', choices=['terminal', 'json'], default='terminal',
                       help='Monitor mode (default: terminal)')
    parser.add_argument('--once', action='store_true',
                       help='Run once and exit (don\'t loop)')
    
    args = parser.parse_args()
    
    monitor = OpenClawMonitor()
    
    if args.mode == 'json':
        data = monitor.get_all_data()
        print(json.dumps(data, indent=2))
    elif args.once:
        monitor.print_terminal_dashboard()
    else:
        print("Press Ctrl+C to exit...")
        try:
            while True:
                monitor.print_terminal_dashboard()
                time.sleep(5)
        except KeyboardInterrupt:
            print("\n👋 Monitor stopped")

if __name__ == "__main__":
    main()