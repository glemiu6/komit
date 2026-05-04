#!/bin/bash
#scripts/uninstall.sh
echo "Uninstalling komit..."
set -e

if command -v komit &> /dev/null; then
  komit-uninstall
else
  sudo rm -f /usr/local/bin/komit
  sudo rm -f /usr/local/bin/komit-update-binary
  git config --global --unset alias.ai 2>/dev/null || true
  rm -rf ~/.config/komit
  echo "komit uninstalled."
fi