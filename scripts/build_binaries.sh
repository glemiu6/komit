#!/bin/bash
#scripts/build_binaries.sh
set -e

OS=$(uname -s)
ARCH=$(uname -s)
echo "Building binaries for $OS/$ARCH..."
pip install pyinstaller

case $OS in
    Linux)
      case $ARCH in
        x86_64)   NAME="komit-linux-x86_64" ;;
        aarch64)  NAME="komit-linux-arm64" ;;
        *)        echo "Unsupported architecture: $ARCH"; exit 1 ;;
      esac
      ;;
    Darwin)
      case $ARCH in
        x86_64)   NAME="komit-macos-x86_64" ;;
        arm64)    NAME="komit-macos-arm64" ;;
        *)        echo "Unsupported architecture: $ARCH"; exit 1 ;;
      esac
      ;;
    *)
      echo "Unsupported OS: $OS"
      exit 1
      ;;
  esac
pyinstaller --onefile komit/main.py --name "$NAME"

echo "binaries in dist/$NAME"
ls -la dist/