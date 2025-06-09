#!/bin/sh
SCRIPT_DIR=$(dirname "$0")
cd "$SCRIPT_DIR" 
source ./venv/bin/activate
./venv/bin/python3 widget.py
