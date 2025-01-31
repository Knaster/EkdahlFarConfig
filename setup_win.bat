@echo off

echo "This will install The Ekdahl FAR Configuration Utility and all of it's needed components, press ctrl+c to abort"
pause

python --version
if %errorlevel% neq 0 (
	echo "Python not installed, install and run again"
	python
	exit /b
)

pip3 install pyside6 pyserial mido python-rtmidi sympy pyqt6-charts

mkdir "C:\Program Files\Ekdahl FAR Configuration Utility"
cd "%~dp0"
cd farconfig
xcopy . "C:\Program Files\Ekdahl FAR Configuration Utility" /E /Y /O

powershell -Command "dir 'C:\Program Files\Ekdahl FAR Configuration Utility\' -s | Unblock-File"

setlocal

:: Set the full path to the batch file you want to run
set "batch_file=C:"\Program Files\Ekdahl FAR Configuration Utility\run_windows.bat"
REM set "batch_file=python3 C:"\Program Files\Ekdahl FAR Configuration Utility\widgegt.py"

:: Set the name for the shortcut
set "shortcut_name=Ekdahl FAR Configuration tool"

:: Create the shortcut in the Start Menu Programs folder
powershell -Command "$s = (New-Object -COM WScript.Shell).CreateShortcut([System.IO.Path]::Combine($env:APPDATA, 'Microsoft\Windows\Start Menu\Programs\%shortcut_name%.lnk')); $s.TargetPath = '%batch_file%'; $s.IconLocation = '	C:\Program Files\Ekdahl FAR Configuration Utility\resources\far_icon.ico'; $s.Save()"

echo Shortcut created in Start Menu.


pause
exit /b
