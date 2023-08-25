#!/bin/sh

CURRENT_DIR=${PWD}
CURRENT_FOLDER=${CURRENT_DIR##*/}
BASE_DIR="git-hooks"
VENV_DIR="$CURRENT_DIR/venv"

if [ ! -f "$CURRENT_DIR/$BASE_DIR/exec-script.sh" ]; then
  echo "Please execute this script from repository root folder."
  exit 1
fi

rm -rf $VENV_DIR
