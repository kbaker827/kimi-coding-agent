#!/usr/bin/env python3
"""
Git Worktree Manager for Parallel Development

Manages isolated git worktrees for parallel Kimi coding sessions.
"""

import os
import subprocess
import shutil
from pathlib import Path
from datetime import datetime


class WorktreeManager:
    """Manage git worktrees for parallel development"""
    
    def __init__(self, repo_path=None):
        self.repo_path = repo_path or os.getcwd()
        self.worktree_base = Path(self.repo_path).parent / '.kimi-worktrees'
        
    def create_worktree(self, name, base_branch='main'):
        """
        Create a new git worktree
        
        Args:
            name: Worktree name (used for directory and branch)
            base_branch: Base branch to checkout from
            
        Returns:
            Path to worktree directory
        """
        worktree_path = self.worktree_base / name
        
        # Ensure worktree base exists
        self.worktree_base.mkdir(parents=True, exist_ok=True)
        
        # Create worktree
        try:
            subprocess.run(
                ['git', 'worktree', 'add', '-b', f'kimi/{name}', str(worktree_path), base_branch],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            print(f"✅ Created worktree: {worktree_path}")
            return str(worktree_path)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create worktree: {e}")
            return None
            
    def list_worktrees(self):
        """List all worktrees"""
        try:
            result = subprocess.run(
                ['git', 'worktree', 'list'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"
            
    def remove_worktree(self, name):
        """Remove a worktree"""
        worktree_path = self.worktree_base / name
        
        try:
            # Remove worktree
            subprocess.run(
                ['git', 'worktree', 'remove', str(worktree_path)],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            print(f"✅ Removed worktree: {worktree_path}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to remove worktree: {e}")
            return False
            
    def cleanup_old(self, days=7):
        """Remove worktrees older than N days"""
        if not self.worktree_base.exists():
            return
            
        now = datetime.now()
        for worktree in self.worktree_base.iterdir():
            if worktree.is_dir():
                stat = worktree.stat()
                age_days = (now - datetime.fromtimestamp(stat.st_mtime)).days
                
                if age_days > days:
                    print(f"🧹 Cleaning up old worktree: {worktree.name} ({age_days} days)")
                    self.remove_worktree(worktree.name)


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Git Worktree Manager')
    parser.add_argument('action', choices=['create', 'list', 'remove', 'cleanup'])
    parser.add_argument('name', nargs='?', help='Worktree name')
    parser.add_argument('--base', '-b', default='main', help='Base branch')
    parser.add_argument('--days', '-d', type=int, default=7, help='Days for cleanup')
    
    args = parser.parse_args()
    
    manager = WorktreeManager()
    
    if args.action == 'create':
        if not args.name:
            print("❌ Worktree name required")
            return 1
        path = manager.create_worktree(args.name, args.base)
        if path:
            print(f"Path: {path}")
        return 0 if path else 1
        
    elif args.action == 'list':
        print(manager.list_worktrees())
        return 0
        
    elif args.action == 'remove':
        if not args.name:
            print("❌ Worktree name required")
            return 1
        return 0 if manager.remove_worktree(args.name) else 1
        
    elif args.action == 'cleanup':
        manager.cleanup_old(args.days)
        return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
