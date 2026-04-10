#!/bin/bash
# Stop hook: verify full CI checks pass before Claude stops working
# Exit code 2 = block (tells Claude to keep working and fix the issue)
# Runs the same checks as GitHub CI: ruff check, ruff format, pyright, pytest, bandit
output=$(make check 2>&1)
if [ $? -ne 0 ]; then
  echo "CI checks are failing. Fix them before stopping:" >&2
  echo "$output" >&2
  exit 2
fi
exit 0
