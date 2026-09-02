@echo off
echo Starting Legal Metrology Compliance Platform...

:: Start Backend in a new window
start "Backend - FastAPI (Port 8000)" cmd /k "cd backend && (if exist venv\Scripts\activate call venv\Scripts\activate) && uvicorn app.main:app --reload --port 8000"

:: Start Frontend in a new window
start "Frontend - Next.js (Port 3000)" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================================
echo   Backend running at:  http://localhost:8000/docs
echo   Frontend running at: http://localhost:3000
echo ========================================================
echo.
