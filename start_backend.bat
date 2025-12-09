@echo off
REM Activate virtual environment
call "%~dp0\venv\Scripts\activate.bat"

echo Starting FastAPI backend on http://0.0.0.0:8000 ...
python -m uvicorn rag_server:app --reload --host 0.0.0.0 --port 8000

pause
