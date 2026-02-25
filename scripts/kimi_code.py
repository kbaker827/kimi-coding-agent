#!/usr/bin/env python3
"""
Kimi Coding Agent - Main CLI

Spawn Kimi K2.5 sub-agents for coding tasks.
"""

import argparse
import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
import uuid


class KimiCodingAgent:
    """Main Kimi coding agent class"""
    
    DEFAULT_MODEL = "moonshot/kimi-k2.5"
    DEFAULT_TIMEOUT = 1800  # 30 minutes
    
    def __init__(self, model=None, workdir=None, timeout=None):
        self.model = model or os.environ.get('KIMI_MODEL', self.DEFAULT_MODEL)
        self.workdir = workdir or os.getcwd()
        self.timeout = timeout or int(os.environ.get('KIMI_TIMEOUT', self.DEFAULT_TIMEOUT))
        self.sessions_dir = Path.home() / '.kimi-coding-agent' / 'sessions'
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        
    def run(self, task, background=False, dry_run=False, **kwargs):
        """
        Run a coding task with Kimi
        
        Args:
            task: The coding task description
            background: Run in background
            dry_run: Preview without executing
            **kwargs: Additional options
            
        Returns:
            Result dict or session info if background
        """
        session_id = str(uuid.uuid4())[:8]
        
        if dry_run:
            print(f"[DRY RUN] Would spawn Kimi session:")
            print(f"  Session ID: {session_id}")
            print(f"  Model: {self.model}")
            print(f"  Workdir: {self.workdir}")
            print(f"  Task: {task[:100]}...")
            return {'dry_run': True, 'session_id': session_id}
            
        # Build the command for sessions_spawn
        spawn_command = self._build_spawn_command(task, session_id, **kwargs)
        
        if background:
            # Run in background using OpenClaw sessions
            return self._run_background(spawn_command, session_id, task)
        else:
            # Run synchronously
            return self._run_sync(spawn_command, session_id, task)
            
    def _build_spawn_command(self, task, session_id, **kwargs):
        """Build the spawn command"""
        max_tokens = kwargs.get('max_tokens', 8192)
        temperature = kwargs.get('temperature', 0.7)
        
        # Enhanced task with system prompt
        enhanced_task = f"""You are an expert software engineer using the Kimi K2.5 model.

WORKING DIRECTORY: {self.workdir}
SESSION ID: {session_id}

TASK:
{task}

INSTRUCTIONS:
1. Work in the specified working directory
2. Make necessary code changes
3. Test your changes if possible
4. Provide a summary of what you did
5. List all files modified or created

Begin working on the task now.
"""
        
        return {
            'task': enhanced_task,
            'model': self.model,
            'timeout': self.timeout,
            'mode': 'run'  # One-shot mode
        }
        
    def _run_sync(self, spawn_command, session_id, task):
        """Run task synchronously"""
        print(f"🚀 Spawning Kimi K2.5 agent...")
        print(f"   Session ID: {session_id}")
        print(f"   Model: {self.model}")
        print(f"   Timeout: {self.timeout}s")
        print()
        
        # Save session info
        session_info = {
            'id': session_id,
            'task': task,
            'model': self.model,
            'workdir': self.workdir,
            'started': datetime.now().isoformat(),
            'status': 'running'
        }
        
        session_file = self.sessions_dir / f"{session_id}.json"
        with open(session_file, 'w') as f:
            json.dump(session_info, f, indent=2)
            
        print(f"⚠️  In OpenClaw, use: sessions_spawn")
        print(f"   Task: {task[:80]}...")
        print()
        print("Run this command in OpenClaw:")
        print(f"sessions_spawn task=\"{task}\" model={self.model}")
        
        return session_info
        
    def _run_background(self, spawn_command, session_id, task):
        """Run task in background"""
        print(f"🚀 Spawning Kimi K2.5 agent in BACKGROUND...")
        print(f"   Session ID: {session_id}")
        print(f"   Model: {self.model}")
        print()
        print("Use these commands to manage:")
        print(f"  Check status: sessions_list")
        print(f"  View logs: sessions_history <session_key>")
        
        return {'session_id': session_id, 'background': True}
        
    def list_sessions(self):
        """List all sessions"""
        sessions = []
        for session_file in self.sessions_dir.glob('*.json'):
            with open(session_file) as f:
                sessions.append(json.load(f))
        return sorted(sessions, key=lambda x: x.get('started', ''), reverse=True)
        
    def get_session(self, session_id):
        """Get session info"""
        session_file = self.sessions_dir / f"{session_id}.json"
        if session_file.exists():
            with open(session_file) as f:
                return json.load(f)
        return None


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Kimi K2.5 Coding Agent',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Quick coding task
  kimi-code "Build a todo app with React"
  
  # Background task
  kimi-code --background "Refactor auth module"
  
  # With specific directory
  kimi-code --workdir ~/my-project "Fix login bug"
  
  # List sessions
  kimi-code --list
  
  # Get session info
  kimi-code --status abc123
        '''
    )
    
    parser.add_argument('task', nargs='?', help='Coding task description')
    parser.add_argument('--background', '-b', action='store_true',
                       help='Run in background')
    parser.add_argument('--workdir', '-w', default='.',
                       help='Working directory (default: current)')
    parser.add_argument('--model', '-m',
                       default=os.environ.get('KIMI_MODEL', 'moonshot/kimi-k2.5'),
                       help='Model to use')
    parser.add_argument('--timeout', '-t', type=int,
                       default=int(os.environ.get('KIMI_TIMEOUT', 1800)),
                       help='Timeout in seconds')
    parser.add_argument('--dry-run', '-n', action='store_true',
                       help='Preview without executing')
    parser.add_argument('--list', '-l', action='store_true',
                       help='List all sessions')
    parser.add_argument('--status', '-s', metavar='SESSION_ID',
                       help='Get session status')
    parser.add_argument('--max-tokens', type=int, default=8192,
                       help='Max tokens for response')
    parser.add_argument('--temperature', type=float, default=0.7,
                       help='Temperature for generation')
    
    args = parser.parse_args()
    
    agent = KimiCodingAgent(
        model=args.model,
        workdir=os.path.abspath(args.workdir),
        timeout=args.timeout
    )
    
    if args.list:
        sessions = agent.list_sessions()
        print("📋 Kimi Coding Sessions:")
        print("-" * 60)
        for s in sessions[:10]:
            status = s.get('status', 'unknown')
            icon = "🟢" if status == 'completed' else "🟡" if status == 'running' else "🔴"
            print(f"{icon} {s['id']} - {s.get('task', 'N/A')[:50]}...")
            print(f"   Started: {s.get('started', 'Unknown')}")
        return 0
        
    if args.status:
        session = agent.get_session(args.status)
        if session:
            print(f"📊 Session: {session['id']}")
            print(f"   Status: {session.get('status', 'Unknown')}")
            print(f"   Task: {session.get('task', 'N/A')[:80]}")
            print(f"   Started: {session.get('started', 'Unknown')}")
        else:
            print(f"❌ Session not found: {args.status}")
        return 0
        
    if not args.task:
        parser.print_help()
        return 1
        
    # Run the task
    result = agent.run(
        task=args.task,
        background=args.background,
        dry_run=args.dry_run,
        max_tokens=args.max_tokens,
        temperature=args.temperature
    )
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
