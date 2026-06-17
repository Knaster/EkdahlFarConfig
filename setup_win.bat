@echo off

echo "This will install The Ekdahl FAR Configuration Utility and all of it's needed components, press ctrl+c to abort"
pause

python --version
if %errorlevel% neq 0 (
	echo "Python not installed, install and run again"
	python
	exit /b
)

pip3 install pyserial pyqt6-charts pyside6 setuptools sympy mido pyinstaller nodegraphqt qt-pyqt-pyside-custom-widgets pycairo cairocffi

mkdir "C:\Program Files\Ekdahl FAR Configuration Utility"
cd "%~dp0"
cd farconfig
xcopy "%~dp0\farconfig" "C:\Program Files\Ekdahl FAR Configuration Utility" /E /Y /O

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

echo downloading and starting GTK+ installer
mkdir "c:\temp"
powershell -Command "curl https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases/download/2022-01-04/gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe -Outfile C:\temp\gtkinst.exe"
powershell -Command "C:\temp\gtkinst.exe"
rm "C:\temp\gtkinst.exe"
rmdir "C:\temp"

pause
exit /b
