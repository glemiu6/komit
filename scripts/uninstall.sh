#!/bin/bash

echo "Uninstalling komit..."

sudo rm -f /usr/local/bin/komit
git config --global --unset alias.ai 2>/dev/null || true

echo "komit uninstalled."