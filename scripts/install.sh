#!/bin/bash
#scripts/install.sh
set -e

OS=$(uname -s)
ARCH=$(uname -m)
REPO="https://github.com/glemiu6/komit"
LATEST=$(curl -fsSL "$REPO/releases/latest" | grep -oP '"tag_name":\s*"\K[^"]+' )

echo "Installing komit $LATEST..."

case $OS in
    Linux)
      case $ARCH in
          x86_64)   BINARY="komit-linux-x86_64" ;;
          aarch64)  BINARY="komit-linux-arm64" ;;
          *)        echo "Unsupported architecture: $ARCH"; exit 1 ;;
      esac
      ;;
    Darwin)
      case $ARCH in
          arm64)    BINARY="komit-macos-arm64" ;;
          *)        echo "Unsupported architecture: $ARCH"; exit 1 ;;
      esac
      ;;
    *)
      echo "Unsupported OS: $OS"
      echo "Try: pip install komit"
      exit 1
      ;;
esac

URL="$REPO/releases/download/$LATEST/$BINARY"
echo "Downloading from $URL..."

curl -fsSL "$URL" -o komit
chmod +x komit
sudo mv komit /usr/local/bin/

echo ""
echo "komit installed successfully!"
echo "Run 'komit' to get started."
echo ""
echo "Setup git alias:"
echo " git config --global alias.ai '!komit'"
echo "Then use: git ai"