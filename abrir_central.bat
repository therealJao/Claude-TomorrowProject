@echo off
rem Abre a Central de Acessos. De dois cliques neste arquivo.
cd /d "%~dp0"

rem Usa o comando py; se ele nao existir (Python da Microsoft Store), usa python.
set PYTHON=py
where py >nul 2>nul || set PYTHON=python

rem Na primeira vez, instala o Pillow (biblioteca de imagens).
%PYTHON% -c "import PIL" 2>nul || %PYTHON% -m pip install pillow
%PYTHON% central.py
if errorlevel 1 pause
