@echo off
REM Change to the backend directory
cd /d "%~dp0"

REM Set the PYTHONPATH to include the current directory
set PYTHONPATH=%cd%

REM Run uvicorn with the correct import path
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 7860