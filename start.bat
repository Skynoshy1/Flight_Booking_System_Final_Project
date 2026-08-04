@echo off
title Flight Booking System Launcher

echo Starting Backend on port 8000...
start "Backend Server" cmd /k "cd backend && .\.venv\Scripts\activate && uvicorn app.main:app --reload --port 8000"

echo Starting Frontend...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo Both services have been started in separate terminals.
pause
