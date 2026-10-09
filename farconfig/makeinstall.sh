python3 -m venv .venv
source .venv/bin/activate
unameOut=$(uname -s)
echo "Installing dependencies, please follow any instructions given"
case "$unameOut" in
    Linux*)     sudo apt install libcairo2-dev pkg-config python3-dev gcc;;
    Darwin*)    brew install cairo pkg-config;;
    *)          echo "Unknown OS: $unameOut" & return;;
esac
#pip3 install pyserial pyside6==6.8.2 setuptools sympy mido pyinstaller nodegraphqt==0.6.43 qt-pyqt-pyside-custom-widgets==2.0.8 pycairo cairocffi
#pip3 install pyserial pyside6==6.11.1 setuptools sympy pyinstaller nodegraphqt==0.6.44 qt-pyqt-pyside-custom-widgets==2.2.1 pycairo cairocffi
pip3 install -r ../requirements.txt
source .venv/bin/activate
pyinstaller farconfig.spec
rm -r .venv
