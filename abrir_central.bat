@echo off
rem Abre a Central de Acessos. De dois cliques neste arquivo.
cd /d "%~dp0"
rem Na primeira vez, instala o Pillow (biblioteca de imagens).
py -c "import PIL" 2>/dev/null || py -m pip install pillow
py central.py
if errorlevel 1 pause
