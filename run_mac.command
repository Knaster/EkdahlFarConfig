#!/bin/sh
SCRIPT_DIR=$(dirname "$0")
cd "$SCRIPT_DIR" 
source / farconfig/./venv/bin/activate
farconfig/./venv/bin/python3 widget.py
