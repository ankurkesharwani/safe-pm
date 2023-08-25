#!/bin/sh

CURRENT_DIR=${PWD}
CURRENT_FOLDER=${CURRENT_DIR##*/}
VENV_DIR="$CURRENT_DIR/venv"

if [ ! -f "$CURRENT_DIR/safe-pm.sh" ]; then
  echo "Please execute this script from the installation directory."
  exit 1
fi

echo "Setting up python virtual environment"

# Setup virtual environment
python3 -m venv "$VENV_DIR"

echo "Setting permissions"
chmod a=rx "clean.sh"
chmod a=rx "safe-pm.sh"
chmod a=rx "setup.sh"

# If requirements.txt does not exist, we are done.
if [ ! -f "requirements.txt" ]; then
    echo "Done"
    exit 0
fi

echo "Installing dependencies"

# Else install dependencies
if [ -d "$VENV_DIR" ]; then

    # Activate python virtual environment
    source "venv/bin/activate"

    # Install dependencies
    pip install -r "requirements.txt"

    # Deactivate virtual environment
    deactivate

    echo "Done"

    # Exit with some status code
    exit 0
else
    echo "Python environment could not be setup properly"
    exit 1
fi
