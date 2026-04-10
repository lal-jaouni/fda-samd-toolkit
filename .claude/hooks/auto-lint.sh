#!/bin/bash
# PostToolUse hook: auto-format and lint after every file edit
# Only runs on Python files
FILE="${CLAUDE_TOOL_INPUT_FILE:-}"
if [[ "$FILE" == *.py ]]; then
  ruff format "$FILE" 2>/dev/null
  ruff check --fix "$FILE" 2>/dev/null
fi
exit 0
