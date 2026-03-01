#!/usr/bin/env python3
"""
OpenClaw Process Monitor - Backend
Real-time dashboard for tracking subagents, processes, and system status
"""

import json
import subprocess
import time
import datetime
from pathlib import Path
import argparse
import sys
import os

class OpenClawMonitor:
    def __init__(self):
        self.workspace = Path.home() / ".openclaw" / "workspace"
        
    def get_subagents(self):
        """Get active subagents via sessions_spawn mechanism"""
        try:
            # In a real implementation, this would call the subagents API
            # For now, we'll simulate calling the OpenClaw API
            result = subprocess.run([
                'openclaw', 'sessions', 'list', '--json'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                sessions_data = json.loads(result.stdout)
                # Filter for subagent sessions
                subagents = []
                for session in sessions_data.get('sessions', []):
                    if 'subagent' in session.get('key', ''):
                        subagents.append({
                            'id': session.get('sessionId', 'unknown'),
                            'name': session.get('displayName', 'Unnamed Subagent'),
                            'status': 'running' if session.get('updatedAt') else 'stopped',
                            'runtime': self._calculate_runtime(session.get('updatedAt', 0)),
                            'model': session.get('model', 'unknown'),
                            'key': session.get('key', ''),
                            'tokens': f"{session.get('totalTokens', 0)}/{session.get('contextTokens', 0)}"
                        })
                return subagents
        except Exception as e:
            print(f"Error fetching subagents: {e}")
            
        return []
        
    def get_background_processes(self):
        """Get background processes"""
        try:
            result = subprocess.run([
                'openclaw', 'sessions', 'list', '--json'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                sessions_data = json.loads(result.stdout)
                processes = []
                for session in sessions_data.get('sessions', []):
                    # Look for sessions that appear to be background processes
                    if any(keyword in session.get('key', '').lower() for keyword in ['cron', 'background']):
                        processes.append({
                            'id': session.get('sessionId', 'unknown'),
                            'name': session.get('displayName', 'Background Process'),
                            'status': 'running' if session.get('updatedAt') else 'stopped',
                            'runtime': self._calculate_runtime(session.get('updatedAt', 0)),
                            'key': session.get('key', ''),
                            'tokens': f"{session.get('totalTokens', 0)}/{session.get('contextTokens', 0)}"
                        })
                return processes
        except Exception as e:
            print(f"Error fetching background processes: {e}")
            
        return []
        
    def get_cron_jobs(self):
        """Get scheduled cron jobs"""
        try:
            result = subprocess.run([
                'openclaw', 'cron', 'list', '--json'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                try:
                    cron_data = json.loads(result.stdout)
                    jobs = []
                    for job in cron_data:
                        next_run = "unknown"
                        if 'state' in job and 'nextRunAtMs' in job['state']:
                            next_run_ms = job['state']['nextRunAtMs']
                            next_run_dt = datetime.datetime.fromtimestamp(next_run_ms / 1000)
                            now = datetime.datetime.now()
                            delta = next_run_dt - now
                            if delta.total_seconds() > 0:
                                next_run = self._format_time_delta(delta)
                            else:
                                next_run = "overdue"
                                
                        jobs.append({
                            'name': job.get('name', 'Unnamed Job'),
                            'schedule': job.get('schedule', {}).get('expr', 'unknown'),
                            'nextRun': next_run,
                            'status': 'enabled' if job.get('enabled', False) else 'disabled',
                            'id': job.get('id', 'unknown')
                        })
                    return jobs
                except json.JSONDecodeError:
                    # Fallback to parsing text output
                    return self._parse_cron_text_output(result.stdout)
        except Exception as e:
            print(f"Error fetching cron jobs: {e}")
            
        return []
        
    def _parse_cron_text_output(self, text_output):
        """Parse cron list text output as fallback"""
        jobs = []
        lines = text_output.strip().split('\n')
        
        for line in lines[1:]:  # Skip header
            if line.strip():
                parts = line.split()
                if len(parts) >= 4:
                    jobs.append({
                        'name': ' '.join(parts[4:]) if len(parts) > 4 else 'Unnamed Job',
                        'schedule': parts[1] if len(parts) > 1 else 'unknown',
                        'nextRun': parts[2] if len(parts) > 2 else 'unknown',
                        'status': parts[3] if len(parts) > 3 else 'unknown',
                        'id': parts[0] if len(parts) > 0 else 'unknown'
                    })
        return jobs
        
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
                    sessions.append({
                        'key': session.get('key', 'unknown'),
                        'channel': session.get('channel', 'unknown'),
                        'age': self._calculate_runtime(session.get('updatedAt', 0)),
                        'tokens': f"{session.get('totalTokens', 0)}/{session.get('contextTokens', 0)}",
                        'model': session.get('model', 'unknown')
                    })
                return sessions
        except Exception as e:
            print(f"Error fetching active sessions: {e}")
            
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
            return f"{minutes}m {seconds}s"
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
                status_icon = "🟢" if agent['status'] == 'running' else "🔴"
                print(f"  {status_icon} {agent['name']}")
                print(f"     Runtime: {agent['runtime']} | Model: {agent['model']}")
                print(f"     Tokens: {agent['tokens']} | ID: {agent['id']}")
        else:
            print("  No active subagents")
            
        # Background Processes
        print(f"\n⚙️ BACKGROUND PROCESSES ({len(data['processes'])}):")
        if data['processes']:
            for proc in data['processes']:
                status_icon = "🟢" if proc['status'] == 'running' else "🔴"
                print(f"  {status_icon} {proc['name']}")
                print(f"     Runtime: {proc['runtime']} | Key: {proc['key']}")
        else:
            print("  No background processes running")
            
        # Cron Jobs
        print(f"\n⏰ SCHEDULED JOBS ({len(data['cronJobs'])}):")
        if data['cronJobs']:
            for job in data['cronJobs']:
                status_icon = "🟢" if job['status'] == 'enabled' else "⏸️"
                print(f"  {status_icon} {job['name']}")
                print(f"     Schedule: {job['schedule']} | Next: {job['nextRun']}")
        else:
            print("  No scheduled jobs configured")
            
        # Active Sessions
        print(f"\n📊 ACTIVE SESSIONS ({len(data['sessions'])}):")
        if data['sessions']:
            for session in data['sessions']:
                print(f"  🔗 {session['channel']} ({session['age']})")
                print(f"     Tokens: {session['tokens']} | Model: {session['model']}")
        else:
            print("  No active sessions")
            
        print("\n" + "=" * 80)
        print("Commands: [R]efresh | [Q]uit | [J]SON export")
        
    def save_json_export(self):
        """Save current data as JSON export"""
        data = self.get_all_data()
        filename = f"openclaw-monitor-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        filepath = self.workspace / "exports" / filename
        filepath.parent.mkdir(exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
            
        print(f"Data exported to: {filepath}")
        return filepath
        
    def interactive_terminal_monitor(self):
        """Run interactive terminal-based monitor"""
        print("Starting OpenClaw Process Monitor...")
        print("Press Ctrl+C to exit")
        
        try:
            while True:
                self.print_terminal_dashboard()
                
                # Simple input handling (non-blocking would be better but this is simpler)
                print("Refreshing in 10 seconds... (press Enter to refresh now)")
                import select
                import sys
                
                # Simple refresh timing
                for i in range(10):
                    time.sleep(1)
                    # Check if there's input available
                    if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                        input_char = sys.stdin.read(1).lower()
                        if input_char == 'q':
                            print("Exiting monitor...")
                            return
                        elif input_char == 'j':
                            self.save_json_export()
                            time.sleep(2)  # Show export message
                        break  # Refresh immediately
                        
        except KeyboardInterrupt:
            print("\nMonitor stopped.")

def main():
    parser = argparse.ArgumentParser(description='OpenClaw Process Monitor')
    parser.add_argument('--mode', choices=['terminal', 'json', 'web'], default='terminal',
                       help='Monitor mode (default: terminal)')
    parser.add_argument('--once', action='store_true',
                       help='Run once and exit (don\'t loop)')
    parser.add_argument('--export', type=str,
                       help='Export data to JSON file')
    
    args = parser.parse_args()
    
    monitor = OpenClawMonitor()
    
    if args.mode == 'json':
        data = monitor.get_all_data()
        print(json.dumps(data, indent=2))
    elif args.export:
        data = monitor.get_all_data()
        with open(args.export, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Data exported to: {args.export}")
    elif args.once:
        monitor.print_terminal_dashboard()
    else:
        monitor.interactive_terminal_monitor()

if __name__ == "__main__":
    main()