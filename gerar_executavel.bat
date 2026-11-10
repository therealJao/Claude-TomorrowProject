@echo off
rem Gera o programa CentralDeAcessos.exe na pasta dist.
cd /d "%~dp0"

set PYTHON=py
where py >nul 2>nul || set PYTHON=python

%PYTHON% -m pip install pillow pyinstaller
%PYTHON% -m PyInstaller --onefile --windowed --name CentralDeAcessos central.py
echo.
echo Pronto! O programa esta em dist\CentralDeAcessos.exe
echo Copie o dados.json para junto dele.
pause
