python3 -m venv .venv
source .venv/bin/activate
#IF MACOS
#	brew install cairo pkg-config
#pip3 install pyserial pyside6==6.8.2 setuptools sympy mido pyinstaller nodegraphqt==0.6.43 qt-pyqt-pyside-custom-widgets==2.0.8 pycairo cairocffi
#pip3 install pyserial pyside6==6.11.1 setuptools sympy pyinstaller nodegraphqt==0.6.44 qt-pyqt-pyside-custom-widgets==2.2.1 pycairo cairocffi
pip3 install -r ../requirements.txt
source .venv/bin/activate
pyinstaller farconfig.spec
rm -r .venv
