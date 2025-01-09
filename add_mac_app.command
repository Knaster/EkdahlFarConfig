#!/bin/bash
SCRIPT_PATH=$(dirname "$0")
cd $SCRIPT_PATH

# Define the application name and paths
APP_NAME="Ekdahl FAR configuration utility"
#SCRIPT_PATH="/path/to/your/script.sh"
APP_DIR="$HOME/Applications/$APP_NAME.app"
CONTENTS_DIR="$APP_DIR/Contents"
MACOS_DIR="$CONTENTS_DIR/MacOS"

# Create the application bundle structure
mkdir -p "$MACOS_DIR"

# Copy the script to the MacOS directory
cp "$SCRIPT_PATH" "$MACOS_DIR/script.sh"

# Make the script executable
chmod +x "$MACOS_DIR/script.sh"

# Create a simple executable to run the script
cat > "$MACOS_DIR/$APP_NAME" << EOF
#!/bin/bash
DIR=\$(dirname "\$0")
\$DIR/script.sh
EOF

# Make the executable run script
chmod +x "$MACOS_DIR/$APP_NAME"

# Create the Info.plist file
cat > "$CONTENTS_DIR/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>$APP_NAME</string>
    <key>CFBundleIdentifier</key>
    <string>com.example.$APP_NAME</string>
    <key>CFBundleName</key>
    <string>$APP_NAME</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
</dict>
</plist>
EOF

# Notify the user
echo "Application $APP_NAME created at $APP_DIR"
