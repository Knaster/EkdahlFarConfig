python3 -m venv .venv
.venv\scripts\activate.bat
pip3 install pyserial pyqt6-charts pyside6 pyserial sympy mido pyinstaller
python3 -m PyInstaller farconfig.spec
