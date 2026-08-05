python3 -m venv .venv
REM .venv\scripts\activate.bat
REM .\.venv\scripts\pip3 install pyserial pyqt6-charts pyside6 setuptools sympy mido pyinstaller nodegraphqt qt-pyqt-pyside-custom-widgets pycairo cairocffi
REM .\.venv\scripts\pip3 install pyserial pyside6==6.11.1 setuptools sympy pyinstaller nodegraphqt==0.6.44 qt-pyqt-pyside-custom-widgets==2.2.1 pycairo cairocffi
.\.venv\scripts\pip3 install -r ..\requirements.txt
.\.venv\scripts\python -m PyInstaller farconfig.spec
