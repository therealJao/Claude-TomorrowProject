@echo off
rem Gera o programa CentralDeAcessos.exe na pasta dist.
cd /d "%~dp0"
py -m pip install pillow pyinstaller
py -m PyInstaller --onefile --windowed --name CentralDeAcessos central.py
echo.
echo Pronto! O programa esta em dist\CentralDeAcessos.exe
pause
