#!/bin/sh
echo "This is the setup program for the Ekdahl FAR Configuration Utility"
echo "The setup requires the installation of homebrew, python3 and various python packages"
read -p "To continue enter "y" and press enter: " response
if [ "$response" != "y" ] ; then
  echo "Aborting"
  exit 1
fi

SCRIPT_DIR=$(dirname "$0")
cd $SCRIPT_DIR
cd farconfig 

APP_NAME="Ekdahl FAR configuration utility"
APP_DIR="/Applications/$APP_NAME.app"
CONTENTS_DIR="$APP_DIR/Contents"
MACOS_DIR="$CONTENTS_DIR/MacOS"
echo "Creating $MACOS_DIR"
mkdir -p "$MACOS_DIR"
mkdir -p "$CONTENTS_DIR/Resources"

cp ./resources/far_icon.icns "$CONTENTS_DIR/Resources/far_icon.icns"
cp -r . "$MACOS_DIR"
chmod +x "run_mac.command"

# Create a simple executable to run the script
#cat > "$MACOS_DIR/$APP_NAME" << EOF
#DIR=\$(dirname "\$0")
#\$DIR/run_mac.command
#EOF

# Make the executable run script
#chmod +x "$MACOS_DIR/$APP_NAME"

# Create the Info.plist file
cat > "$CONTENTS_DIR/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>run_mac.command</string>
    <key>CFBundleIconFile</key>
    <string>far_icon</string>
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

if ! command -v brew &> /dev/null; then
	echo "Installing homebrew"
	bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
	echo "Homebrew allready installed, skipping"
fi

if ! echo "$PATH" | grep -q "/opt/homebrew/bin"; then
	echo "Updating PATH"
	export PATH="/opt/homebrew/bin:$PATH"
	echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.bash_profile
	echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
fi
if ! echo "$PATH" | grep -q "/usr/local/bin"; then
	echo "Updating PATH"
	export PATH="/usr/local/bin:$PATH"
	echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bash_profile
	echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zshrc
fi

brew update

if which /usr/local/bin/python3 &> /dev/null; then
	python_version=$(/usr/local/bin/python3 --version | awk '{print $2}')
	python_major_version=$(echo $python_version | cut -d'.' -f1)
	python_minor_version=$(echo $python_version | cut -d'.' -f2)

	if [[ $python_major_version -ge 3 && $python_minor_version -ge 10 ]]; then
		echo "Python 3.10 or higher found, skipping install"
	else
		brew install python
	fi
else
	echo "Installing python 3.10 or higher"
	brew install python
fi

python_path=$(brew --prefix python)/libexec/bin/python
pip_path=$(brew --prefix python)/libexec/bin/pip

#Echo "Python version"
#$python_path --version

source ~/.bash_profile
source ~/.zshrc

cd "$MACOS_DIR"
echo "Current directory"
echo $(dirname "$0")
#$python_path --version

#if [ ! -d "$MACOS_DIR/venv" ]; then
	echo "Creating python virtual environment"
	$python_path -m venv "$MACOS_DIR/venv"
#fi

source "$MACOS_DIR/venv/bin/activate"

echo "Installing python packages"

./venv/bin/pip install pyserial pyqt6-charts pyside6 pyserial mido sympy

read -p "All done! Press Enter to quit"

deactivate
