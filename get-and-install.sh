#!/bin/bash

set -e

# === Step 1: Validate input ===

if [ -z "$1" ]; then
  echo "❌ Error: You must provide a folder path to clone the repository into."
  echo "Usage: bash <(curl -s https://raw.githubusercontent.com/ankurkesharwani/safe-pm/main/get-and-install.sh) /path/to/folder"
  exit 1
fi

PARENT_DIR="$1"
TARGET_DIR="$PARENT_DIR/SafePM"

if [ ! -d "$PARENT_DIR" ]; then
  echo "❌ Error: The folder '$PARENT_DIR' does not exist."
  echo "Please create it first or provide a valid path."
  exit 1
fi

if [ ! -d "$TARGET_DIR" ]; then
  mkdir $TARGET_DIR
fi

# === Step 2: Define variables ===

REPO_URL="https://github.com/ankurkesharwani/safe-pm.git"

# === Step 3: Clone repo ===

echo "📥 Cloning SafePM into: $TARGET_DIR"
git clone "$REPO_URL" "$TARGET_DIR"

# === Step 4: Run installer ===

cd "$TARGET_DIR" || exit 1

echo "⚙️ Running SafePM installer"
chmod +x ./install
./install

# === Step 5: Cleanup ===

echo "🧹 Cleaning up .git folder and get-and-install.sh..."

rm -rf .git
[ -f get-and-install.sh ] && rm get-and-install.sh

echo "✅ Installation complete. SafePM is ready to use."
