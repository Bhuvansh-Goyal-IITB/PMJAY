@echo off
REM Run the clean script
call clean.bat

REM Run PyInstaller to build the executable
pyinstaller --noconsole --clean -n PMJAY --onefile --icon assets\app_icon.ico --hidden-import=babel.numbers main.py

REM Copy the assets folder to the dist directory
xcopy "assets" "dist\assets" /E /I /Q /Y

REM Compress the dist folder
powershell -Command "Compress-Archive .\dist\* PMJAY.zip"

echo Build complete.