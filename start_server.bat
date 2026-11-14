@echo off
title Smart City Traffic Backend Server
echo ========================================================
echo Starting Smart City Traffic Monitoring Backend Server...
echo ========================================================
cd /d "%~dp0"
python app.py
pause
