#!/bin/sh

CURRENT_DIR=${PWD}

if [ ! -f "$CURRENT_DIR/safe-pm.sh" ]; then
  echo "Please execute this from installation dir."
  exit 1
fi

VENV_DIR="$CURRENT_DIR/venv"

if [ -d "$VENV_DIR" ]; then

    # Activate python virtual environment
    source "$VENV_DIR/bin/activate"

    # Execute the script passed as param
    python "$1" ${@:2}
    EXIT_CODE=$?

    # Deactivate virtual environment
    deactivate

    # Exit with some status code
    echo "Exiting with code: $EXIT_CODE\n"
    exit $EXIT_CODE
else
    echo "Python environment is not setup. Please run \`setup.sh\` first".
    exit 1
fi
