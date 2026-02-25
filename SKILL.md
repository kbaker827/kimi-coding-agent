---
name: kimi-coding-agent
description: Delegate coding tasks to Kimi K2.5 via background sub-agents. Use for building features, refactoring code, code review, debugging, and complex coding workflows. Spawn isolated Kimi sessions that work independently and report back results. Triggers - coding with kimi, use kimi for code, spawn kimi agent, delegate to kimi.
---

# Kimi K2.5 Coding Agent

**Spawn Kimi K2.5 sub-agents for coding tasks.**

## What It Does

Launches isolated Kimi K2.5 coding sessions that:
- ✅ Build new features and applications
- ✅ Refactor existing code
- ✅ Review pull requests
- ✅ Debug complex issues
- ✅ Write tests and documentation

## When to Use

| Use Kimi Coding Agent | Don't Use |
|----------------------|-----------|
| Building new features | One-liner fixes |
| Refactoring large codebases | Simple edits |
| Complex debugging | Reading code |
| Multi-file changes | Quick questions |
| Code review | Already know the fix |

## Quick Start

### One-Shot Coding Task

```python
# Spawn Kimi to build a feature
kimi-code "Build a REST API for user authentication with JWT tokens"

# Refactor code
kimi-code "Refactor the database layer to use async/await"

# Write tests
kimi-code "Write unit tests for the payment module"
```

### Background Session

```python
# Start long-running task
kimi-code --background "Implement a caching layer with Redis"

# Check progress
kimi-status <session-id>

# View logs
kimi-logs <session-id>
```

### Multi-Agent Parallel Work

```python
# Fix multiple issues simultaneously
kimi-code --worktree issue-123 "Fix login bug"
kimi-code --worktree issue-124 "Update dashboard UI"
kimi-code --worktree issue-125 "Optimize queries"
```

## CLI Commands

```bash
# Quick task (waits for completion)
kimi-code "Your coding task"

# Background task (returns immediately)
kimi-code --background "Your task"

# With specific model variant
kimi-code --model kimi-k2.5 "Your task"

# With timeout
kimi-code --timeout 1800 "Your task"  # 30 minutes

# Dry run (preview what would happen)
kimi-code --dry-run "Your task"
```

## Python API

```python
from kimi_coding_agent import KimiCodingAgent

# Initialize agent
agent = KimiCodingAgent(
    model="moonshot/kimi-k2.5",
    workdir="~/my-project"
)

# Run task
result = agent.run("Build a todo app with React")

# Or run in background
session = agent.run_background("Refactor auth module")

# Check status
status = agent.get_status(session.id)

# Get results
output = agent.get_output(session.id)
```

## Features

### 🧠 Kimi K2.5 Powered
- Long context window (256K tokens)
- Excellent code understanding
- Strong reasoning capabilities
- Multi-language support

### 🔄 Session Management
- Background execution
- Progress monitoring
- Log streaming
- Graceful cancellation

### 🌳 Worktree Support
- Parallel development
- Isolated environments
- Git worktree integration
- Clean workspace per task

### 📊 Output Tracking
- Real-time logs
- File change detection
- Result summarization
- Error reporting

## Configuration

### Environment Variables

```bash
export KIMI_MODEL="moonshot/kimi-k2.5"
export KIMI_TIMEOUT="1800"
export KIMI_MAX_TOKENS="8192"
export KIMI_TEMPERATURE="0.7"
```

### Config File

Create `~/.kimi-coding-agent/config.yaml`:

```yaml
model: moonshot/kimi-k2.5
default_timeout: 1800
max_tokens: 8192
temperature: 0.7
auto_approve: false
notify_on_complete: true
```

## Safety Features

- ✅ **Isolated Sessions** - Each task runs in separate context
- ✅ **Git Integration** - Changes tracked in git worktrees
- ✅ **Dry Run Mode** - Preview before execution
- ✅ **Timeout Limits** - Prevents runaway sessions
- ✅ **Approval Gates** - Review before major changes

## Scripts

- `scripts/kimi_code.py` - Main CLI interface
- `scripts/kimi_agent.py` - Agent management
- `scripts/worktree_manager.py` - Git worktree utilities
- `scripts/session_monitor.py` - Monitor active sessions

## Best Practices

### Task Description Tips

**Good:**
```
"Refactor the UserService class to use dependency injection.
Move database calls to a UserRepository class.
Keep all existing tests passing."
```

**Bad:**
```
"Fix the code"
```

### Handling Large Tasks

Break into smaller chunks:
```python
# Phase 1: Design
kimi-code "Design the API schema for a blog platform"

# Phase 2: Implement
kimi-code "Implement the API based on the design doc"

# Phase 3: Test
kimi-code "Write tests for the blog API"
```

### Reviewing Results

Always review Kimi's output:
```python
# Check what changed
kimi-review <session-id>

# View diff
kimi-diff <session-id>

# Approve changes
kimi-approve <session-id>
```

## Examples

### Build a Feature

```bash
kimi-code "Build a pagination component for the user list.
Use React with TypeScript.
Include previous/next buttons and page numbers.
Style with Tailwind CSS."
```

### Refactor Legacy Code

```bash
kimi-code "Refactor the legacy payment processor.
Convert callbacks to async/await.
Add proper error handling.
Maintain backward compatibility."
```

### Code Review

```bash
kimi-code --pr 456 "Review this PR for security issues.
Focus on authentication and input validation.
Suggest improvements."
```

### Fix Bug

```bash
kimi-code "Fix the race condition in the order processing.
The issue occurs when two orders update inventory simultaneously.
Add proper locking or atomic operations."
```

## Troubleshooting

### Session Hangs

```bash
# Check status
kimi-status <session-id>

# Kill if stuck
kimi-kill <session-id>

# Restart with timeout
kimi-code --timeout 600 "Task"
```

### Out of Context

If task is too large:
```bash
# Use file references
kimi-code --files "src/auth.js,src/users.js" "Refactor auth"

# Or break into parts
kimi-code "Part 1: Extract utilities"
kimi-code "Part 2: Refactor main logic"
```

### Model Errors

```bash
# Try with different settings
kimi-code --temperature 0.5 --max-tokens 4096 "Task"
```

## Comparison

| Feature | Kimi Agent | Codex | Claude Code |
|---------|-----------|-------|-------------|
| Context | 256K | 200K | 200K |
| Speed | Fast | Medium | Medium |
| Cost | Low | Medium | High |
| Code Quality | Excellent | Excellent | Excellent |
| Best For | Large refactor | Quick fixes | Complex design |

## References

- `references/prompting_guide.md` - Kimi prompting best practices
- `references/session_patterns.md` - Session management patterns
- `references/troubleshooting.md` - Common issues and solutions
