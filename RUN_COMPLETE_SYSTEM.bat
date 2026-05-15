@echo off
REM CASE Tool - Complete Backend + Frontend Startup Script
REM This script starts both the backend FastAPI server and the frontend dev server

echo ========================================
echo CASE Tool - Starting Complete System
echo ========================================
echo.

REM Check if backend venv exists
if not exist "backend\venv" (
    echo Creating Python virtual environment...
    cd backend
    python -m venv venv
    cd ..
)

REM Start backend
echo.
echo Starting Backend Server...
echo Backend will run on: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
start cmd /k "cd backend && .\venv\Scripts\python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to start
timeout /t 3 /nobreak

REM Start frontend
echo.
echo Starting Frontend Server...
echo Frontend will run on: http://localhost:5500
echo.
start cmd /k "cd frontend && python -m http.server 5500 --directory ."

echo.
echo ========================================
echo CASE Tool is starting!
echo ========================================
echo.
echo Frontend: http://localhost:5500
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Default Credentials (create your first project):
echo Email: admin@example.com
echo Password: admin123
echo.
echo Note: You may need to register a new user or use the API to create the first admin user.
echo.
timeout /t 5
