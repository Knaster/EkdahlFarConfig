#!/bin/sh
sed -E 's/([[:space:]]*)self\.(\w+):[[:space:]]*([^=]+)=/\1## \3\n\1self.\2=/' "$1"
