#!/bin/bash
#scripts/uninstall.sh
echo "Uninstalling komit..."

sudo rm -f /usr/local/bin/komit
sudo rm -f /usr/local/bin/komit-update
git config --global --unset alias.ai 2>/dev/null || true

echo "komit uninstalled."