#!/bin/bash
set -e

REPO="https://github.com/glemiu6/komit"
detect_platform() {
  OS=$(uname -s)
  ARCH=$(uname -m)

  case $OS in
      Linux)
        case $ARCH in
          x86_64)   BINARY="komit-linux-x86_64" ;;
          aarch64)  BINARY="komit-linux-arm64" ;;
          *)        echo "Unsupported architecture: $ARCH"; exit 1 ;;
        esac
        INSTALL_DIR="/usr/local/bin"
        ;;
      Darwin)
        case $ARCH in
          arm64)
            BINARY="komit-macos-arm64"
            INSTALL_DIR="/opt/homebrew/bin"
            ;;
          x86_64)
            echo "Intel Mac binary not available. Use: pip install komit"
            exit 1
            ;;
          *)      echo "Unsupported architecture: $ARCH"; exit 1 ;;
        esac
        ;;
      *)
        echo "Unsupported OS: $OS. Use: pip install komit"
        exit 1
        ;;
  esac

}

get_latest_version() {
  LATEST=$(curl -fsSL "https://api.github.com/repos/glemiu6/komit/releases/latest" | grep '"tag_name"' | sed 's/.*"tag_name": *"\([^"]*\)".*/\1/')
  # PyPI fallback
  if [ -z "$LATEST" ]; then
    LATEST=$(curl -fsSL "https://pypi.org/pypi/komit/json" | grep -o '"version":"[^"]*"' | head -1 | sed 's/"version":"//;s/"//')
    LATEST="v$LATEST"
  fi

  if [ -z "$LATEST" ]; then
    echo "Error: could not determine latest version."
    exit 1
  fi
}
download_binary() {
  URL="$REPO/releases/download/$LATEST/$BINARY"
  echo "Downloading from $URL..."
  curl -L --progress-bar "$URL" -o komit
  if [ $? -ne 0 ] || [ ! -s komit ]; then
    rm -f komit
    exit 1
  fi
  chmod +x komit
  if [ ! -d "$INSTALL_DIR" ]; then
    echo "Creating $INSTALL_DIR..."
    sudo mkdir -p "$INSTALL_DIR"
  fi
  sudo mv komit "$INSTALL_DIR/"
  echo "Installed to $INSTALL_DIR/komit"
}


print_success() {
  echo ""
  echo "komit $LATEST installed successfully"
  echo ""
  echo "Run 'komit' to get started"
  echo "Run 'komit init' to setup a config file"
  echo "Run 'komit update' to update"
  echo "Run 'komit uninstall' to uninstall"
  echo ""
  echo "Setup git alias:"
  echo "  git config --global alias.ai '!komit'"
  echo "Then use: git ai"
}

detect_platform
get_latest_version
echo "Installing komit $LATEST"
download_binary
print_success