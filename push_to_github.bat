@echo off
title Push to GitHub Repository
echo ========================================================
echo Pushing Smart City Traffic Project to GitHub...
echo ========================================================
cd /d "%~dp0"
git remote remove origin 2>nul
git remote add origin https://github.com/KMRakshithGowda/Smart-City-Traffic-Monitoring-System.git
git push -u origin main
echo ========================================================
echo Done! Check your GitHub repository.
echo ========================================================
pause
