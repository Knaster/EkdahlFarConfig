python3 -m venv .venv
REM .venv\scripts\activate.bat
.\.venv\scripts\pip3 install pyserial pyqt6-charts pyside6 setuptools sympy mido pyinstaller nodegraphqt qt-pyqt-pyside-custom-widgets pycairo cairocffi
.\.venv\scripts\python -m PyInstaller farconfig.spec
