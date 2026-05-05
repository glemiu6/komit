#!/bin/bash
#scripts/uninstall.sh
echo "Uninstalling komit..."
set -e

sudo rm -f /usr/local/bin/komit
git config --global --unset alias.ai 2>/dev/null || true
rm -rf ~/.config/komit
echo "komit uninstalled."