@echo off
setlocal
where gradle >nul 2>nul
if errorlevel 1 (
  echo Gradle is not installed or not on PATH. Install Gradle or generate the official Gradle wrapper before building.
  exit /b 1
)
gradle %*
