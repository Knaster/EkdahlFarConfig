python3 -m venv .venv
source .venv/bin/activate
pip3 install pyserial pyqt6-charts pyside6 pyserial sympy mido pyinstaller
pyinstaller farconfig.spec
