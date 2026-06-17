python3 -m venv .venv
source .venv/bin/activate
pip3 install pyserial pyqt6-charts pyside6 setuptools sympy mido pyinstaller nodegraphqt qt-pyqt-pyside-custom-widgets pycairo cairocffi
pyinstaller farconfig.spec
