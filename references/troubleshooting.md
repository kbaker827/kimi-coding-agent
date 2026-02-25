# Troubleshooting

## Common Issues

### Session Timeout
Increase timeout:
```bash
kimi-code --timeout 3600 "task"
```

### Out of Context
Break into smaller tasks or use file references.

### Model Errors
Try with different temperature:
```bash
kimi-code --temperature 0.5 "task"
```

## Getting Help

- Check session logs: `kimi-monitor show <id>`
- Review output files in `~/.kimi-coding-agent/sessions/`
- Run with `--dry-run` to preview
