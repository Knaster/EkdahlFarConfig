This is the Ekdahl FAR Configuration software 
(https://github.com/Knaster/EkdahlFarConfig)

This software has been tested on Linux (Ubuntu 22.04), Windows (11) and Mac (Ventura, Sequoia) . 
It should be considered to be in beta stage as 99% of intial functionality is there but it needs to be thoroughly tested.

Initial installation procedures has been added but further testing is required.

Please be adviced that the organization and structure of this code is TERRIBLE since i am not a Qt/Python guy and i
only learned as much as i needed to get everything working. Cleanup and restructuring is most certainly necessary.
The code has been developed using the Community version of PyCharm 2023.3.4, forms have been compiled with
QT Creator 12.0.1.

By default this code will essentially do nothing until connected to a Teensy 4.0 with the Ekdahl FAR firmware

---------------------

Installation
---------------------
All OS's:
	
An internet connection will be required during setup of the software.
Python 3.10 or later is required for ALL operating systems, some installers may attempt to install it if not found
- Download and extract the files from the github repository

MacOS:
- run 'setup_mac.command' from finder
!!If you get the message "'setup_mac.command' was not opened" and some crap about malware !!
This is due to apples forever gatekeeping against independent and not-for-profit software development.
To circumvent this, if you have tried to run the file once you can go to the apple menu at the top left
and choose "system settings", here scroll down to "privacy & security" and it will say
"'setup_mac.command' was blocked to protect your mac' - press "Open Anyway" to continue the installer.
If at the end of the installer you get a bunch of errors about not finding 'brew' because it's not in PATH,
just let it finish, close the installer and run it again from Finder. 

The script will install Handbrake (if not present) which in turn will install Python 3.10 or later and the required python dependencies.
It will also copy the program files to '/Applications/Ekdahl FAR Configuration Utility' and create a launcher icon

Windows:
- Left-click on 'setup_win.bat' in the directory where the files have been extracted
  then right-click on it and choose 'properties'. On the bottom right check the 'unblock' box and press OK.
- Right-click on it again and choose 'run as administrator' and click 'yes'
If Python is not installed, this will launch the Python installer and exit and you have to run it again. 
First all python depencies are installed, then it will copy the program files to
'C:\Program Files\Ekdahl FAR Configuration Utility' and create an icon in the start menu.

Linux:
Start a terminal in the directory where you've extracted the files and do
$ sudo apt update
$ sudo apt install python
(make sure it installs python 3.10 or later!)

To install in a virtual python environment:
$ python3 -m venv ./venv
$ ./venv/bin/pip3 install pyside6 pyserial mido python-rtmidi sympy pyqt6-charts

To run through the virtual environment:
./run_linux.sh
(runs ./venv/bin/python3 widget.py)


Dependencies
---------------------
This software requires Python 3.10 or higher, it can be downloaded for all platforms on https://www.python.org

The software also requires a number of python packages;

pyside6
pyserial
mido
python-rtmidi
sympy
pyqt6-charts
