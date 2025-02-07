python3 -m venv .venv
REM .venv\scripts\activate.bat
.\.venv\scripts\pip3 install pyserial pyqt6-charts pyside6 pyserial sympy mido pyinstaller
.\.venv\scripts\python -m PyInstaller farconfig.spec
