# Kimi K2.5 Coding Agent

**Spawn Kimi K2.5 sub-agents for coding tasks.**

A powerful coding agent skill for OpenClaw that leverages Kimi K2.5's 256K context window and excellent code understanding capabilities.

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/kbaker827/kimi-coding-agent.git
cd kimi-coding-agent

# Install launcher
chmod +x scripts/kimi_code.py
ln -s $(pwd)/scripts/kimi_code.py ~/.local/bin/kimi-code
```

### First Task

```bash
# Simple coding task
kimi-code "Build a Python CLI tool for converting CSV to JSON"

# Or with specific directory
kimi-code --workdir ~/my-project "Refactor the database layer"
```

## 💡 Usage Examples

### Building Features

```bash
# Build a React component
kimi-code "Build a pagination component for a user list.
Use TypeScript, Tailwind CSS, and include tests."

# Create an API endpoint
kimi-code "Create a REST endpoint for user authentication
with JWT tokens, bcrypt password hashing, and input validation."
```

### Refactoring

```bash
# Refactor legacy code
kimi-code "Convert the callback-based payment processor
to use async/await with proper error handling."

# Extract components
kimi-code "Extract the data fetching logic into a custom hook
called useApi that handles loading and error states."
```

### Code Review

```bash
# Review a PR
kimi-code "Review this code for security issues.
Focus on SQL injection vulnerabilities and XSS attacks."

# Check for best practices
kimi-code "Check if this code follows Python best practices
and suggest improvements."
```

### Parallel Development

```bash
# Create worktrees for parallel work
kimi-worktree create feature-auth
kimi-worktree create feature-dashboard

# Spawn agents in parallel
kimi-code --worktree ~/.kimi-worktrees/feature-auth "Implement JWT auth"
kimi-code --worktree ~/.kimi-worktrees/feature-dashboard "Build dashboard UI"

# Monitor both
kimi-monitor --summary
```

## 🎯 Features

### Core Features

- ✅ **256K Context Window** - Handle large codebases
- ✅ **Background Sessions** - Run long tasks without blocking
- ✅ **Worktree Support** - Parallel development with git worktrees
- ✅ **Session Monitoring** - Track progress of running agents
- ✅ **Dry Run Mode** - Preview before executing
- ✅ **Timeout Control** - Prevent runaway sessions

### Safety Features

- ✅ **Isolated Sessions** - Each agent runs independently
- ✅ **Git Integration** - Changes tracked in worktrees
- ✅ **Approval Gates** - Review changes before applying
- ✅ **Output Logging** - Full trace of agent actions

## 🖥️ Commands

### Main Commands

| Command | Description |
|---------|-------------|
| `kimi-code "task"` | Run coding task |
| `kimi-code --background "task"` | Run in background |
| `kimi-code --list` | List all sessions |
| `kimi-code --status <id>` | Get session info |
| `kimi-worktree create <name>` | Create git worktree |
| `kimi-worktree list` | List worktrees |
| `kimi-monitor summary` | View all sessions |
| `kimi-monitor watch <id>` | Watch live progress |

### Options

```bash
kimi-code [OPTIONS] "TASK"

Options:
  -b, --background        Run in background
  -w, --workdir PATH      Set working directory
  -m, --model MODEL       Use specific model (default: moonshot/kimi-k2.5)
  -t, --timeout SECONDS   Set timeout (default: 1800)
  -n, --dry-run          Preview without executing
  --max-tokens N          Max tokens for response (default: 8192)
  --temperature FLOAT     Temperature 0.0-1.0 (default: 0.7)
```

## 🐍 Python API

```python
from kimi_coding_agent import KimiCodingAgent

# Initialize agent
agent = KimiCodingAgent(
    model="moonshot/kimi-k2.5",
    workdir="~/my-project",
    timeout=1800
)

# Run task synchronously
result = agent.run("Build a REST API")

# Or in background
session = agent.run("Refactor auth", background=True)

# Monitor progress
from scripts.session_monitor import SessionMonitor
monitor = SessionMonitor()
monitor.watch_session(session['session_id'])
```

## ⚙️ Configuration

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

## 📁 File Structure

```
kimi-coding-agent/
├── SKILL.md                    # Skill documentation
├── README.md                   # This file
├── scripts/
│   ├── kimi_code.py           # Main CLI (160 lines)
│   ├── worktree_manager.py    # Git worktree utils
│   └── session_monitor.py     # Session monitoring
└── references/
    ├── prompting_guide.md     # Prompting best practices
    └── troubleshooting.md     # Common issues
```

## 🔧 Troubleshooting

### Session Not Starting

```bash
# Check model availability
kimi-code --dry-run "test"

# Try with explicit model
kimi-code --model moonshot/kimi-k2.5 "task"
```

### Out of Context

If your task is too large:

```bash
# Break into smaller tasks
kimi-code "Part 1: Design the database schema"
kimi-code "Part 2: Implement the API endpoints"
kimi-code "Part 3: Write tests"
```

### Session Hangs

```bash
# Check status
kimi-code --status <session-id>

# Watch progress
kimi-monitor watch <session-id>

# Kill if needed
# (Use sessions_list and sessions_kill in OpenClaw)
```

## 📊 Comparison

| Feature | Kimi K2.5 | GPT-4 | Claude 3.5 |
|---------|-----------|-------|------------|
| Context | 256K | 128K | 200K |
| Code Quality | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Speed | Fast | Medium | Medium |
| Cost | $ | $$$ | $$ |

## ⚠️ Best Practices

### Writing Good Tasks

**✅ Good:**
```
"Refactor the UserService class to use dependency injection.
Move all database calls to a UserRepository class.
Keep all existing tests passing."
```

**❌ Bad:**
```
"Fix the code"
```

### Task Size

- **Small**: 1-3 files, < 30 min
- **Medium**: Component-level, < 1 hour
- **Large**: Architecture changes, > 1 hour (use worktrees)

### Parallel Work

```bash
# Good for parallel tasks
kimi-code --worktree feature-1 "Task A" &
kimi-code --worktree feature-2 "Task B" &
kimi-code --worktree feature-3 "Task C" &
wait
```

## 🤝 Contributing

Found a bug or have a feature request? Open an issue or PR!

## 📄 License

MIT License - See LICENSE file

## 🔗 Links

- **Repository:** https://github.com/kbaker827/kimi-coding-agent
- **Kimi AI:** https://www.moonshot.cn
- **OpenClaw:** https://docs.openclaw.ai

---

**Code smarter with Kimi K2.5! 🚀**
