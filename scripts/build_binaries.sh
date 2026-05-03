#!/bin/bash
set -e

echo "Building binaries..."
pip install pyinstaller

pyinstaller --onefile komit/main.py --name komit-linux-x86_64
pyinstaller --onefile komit/main.py --name komit-macos-arm64

echo "binaries in dist/"
ls -la dist/