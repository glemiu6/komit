#!/bin/bash

if command -v komit &> /dev/null; then
  komit
elif command -v python3 &> /dev/null; then
  python3 -m komit
else
  echo "komit not found. Install with:"
  echo "  curl -fsSL https://raw.githubusercontent.com/glemiu6/komit/main/scripts/install.sh | bash"
  echo "  or: pip install komit"
  exit 1
fi