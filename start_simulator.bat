@echo off
title Smart City IoT Traffic Simulator
echo ========================================================
echo Starting Smart City IoT Traffic Simulator...
echo Streaming sensor telemetry to http://127.0.0.1:5000/api/ingest
echo ========================================================
cd /d "%~dp0"
python simulator.py --interval 3
pause
