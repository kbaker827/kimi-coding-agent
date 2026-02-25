#!/usr/bin/env python3
"""
Session Monitor for Kimi Coding Agents

Monitor active Kimi coding sessions and their progress.
"""

import json
import time
from pathlib import Path
from datetime import datetime


class SessionMonitor:
    """Monitor Kimi coding sessions"""
    
    def __init__(self):
        self.sessions_dir = Path.home() / '.kimi-coding-agent' / 'sessions'
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        
    def list_sessions(self, status=None):
        """List all sessions"""
        sessions = []
        
        for session_file in self.sessions_dir.glob('*.json'):
            try:
                with open(session_file) as f:
                    session = json.load(f)
                    if status is None or session.get('status') == status:
                        sessions.append(session)
            except:
                pass
                
        return sorted(sessions, key=lambda x: x.get('started', ''), reverse=True)
        
    def get_session(self, session_id):
        """Get specific session"""
        session_file = self.sessions_dir / f"{session_id}.json"
        if session_file.exists():
            with open(session_file) as f:
                return json.load(f)
        return None
        
    def update_session(self, session_id, updates):
        """Update session info"""
        session = self.get_session(session_id)
        if session:
            session.update(updates)
            session['updated'] = datetime.now().isoformat()
            
            session_file = self.sessions_dir / f"{session_id}.json"
            with open(session_file, 'w') as f:
                json.dump(session, f, indent=2)
                
    def watch_session(self, session_id, interval=5):
        """Watch a session for updates"""
        print(f"👁️  Watching session: {session_id}")
        print(f"   Refresh every {interval}s (Ctrl+C to stop)")
        print()
        
        last_status = None
        
        try:
            while True:
                session = self.get_session(session_id)
                
                if not session:
                    print(f"❌ Session not found: {session_id}")
                    break
                    
                status = session.get('status', 'unknown')
                
                if status != last_status:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Status: {status}")
                    
                    if status == 'completed':
                        print("✅ Session completed!")
                        print(f"   Output: {session.get('output_file', 'N/A')}")
                        break
                    elif status == 'failed':
                        print("❌ Session failed!")
                        print(f"   Error: {session.get('error', 'Unknown')}")
                        break
                        
                last_status = status
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n👋 Stopped watching")
            
    def display_summary(self):
        """Display summary of all sessions"""
        sessions = self.list_sessions()
        
        print("📊 Kimi Coding Sessions Summary")
        print("=" * 60)
        
        running = [s for s in sessions if s.get('status') == 'running']
        completed = [s for s in sessions if s.get('status') == 'completed']
        failed = [s for s in sessions if s.get('status') == 'failed']
        
        print(f"\n🟢 Running: {len(running)}")
        for s in running:
            print(f"   - {s['id']}: {s.get('task', 'N/A')[:40]}...")
            
        print(f"\n✅ Completed: {len(completed)}")
        print(f"❌ Failed: {len(failed)}")
        print(f"📁 Total: {len(sessions)}")


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Session Monitor')
    parser.add_argument('action', choices=['list', 'watch', 'summary', 'show'])
    parser.add_argument('session_id', nargs='?', help='Session ID')
    parser.add_argument('--interval', '-i', type=int, default=5,
                       help='Watch interval in seconds')
    parser.add_argument('--status', '-s', choices=['running', 'completed', 'failed'],
                       help='Filter by status')
    
    args = parser.parse_args()
    
    monitor = SessionMonitor()
    
    if args.action == 'list':
        sessions = monitor.list_sessions(args.status)
        print(f"📋 Sessions ({len(sessions)} total):")
        for s in sessions:
            icon = {"running": "🟢", "completed": "✅", "failed": "❌"}.get(s.get('status'), "⚪")
            print(f"{icon} {s['id']} - {s.get('task', 'N/A')[:50]}...")
            
    elif args.action == 'watch':
        if not args.session_id:
            print("❌ Session ID required")
            return 1
        monitor.watch_session(args.session_id, args.interval)
        
    elif args.action == 'summary':
        monitor.display_summary()
        
    elif args.action == 'show':
        if not args.session_id:
            print("❌ Session ID required")
            return 1
        session = monitor.get_session(args.session_id)
        if session:
            print(json.dumps(session, indent=2))
        else:
            print(f"❌ Session not found: {args.session_id}")
            return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
