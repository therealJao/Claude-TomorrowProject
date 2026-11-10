@echo off
rem Abre a Central de Acessos. De dois cliques neste arquivo.
cd /d "%~dp0"
py central.py
if errorlevel 1 pause
