@echo off
REM Setup script for Windows
echo ============================================================
echo Django HoneyPot Sample - Project Setup (Windows)
echo ============================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH.
    exit /b 1
)

echo Python found!

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment.
        exit /b 1
    )
    echo Virtual environment created!
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment and install requirements
echo Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install requirements.
    exit /b 1
)
echo Dependencies installed!

REM Copy .env.example to .env if .env doesn't exist
if not exist ".env" (
    if exist ".env.example" (
        echo Copying .env.example to .env...
        copy .env.example .env
        echo Please edit .env file with your configuration.
    ) else (
        echo Warning: .env.example not found. Please create .env manually.
    )
)

REM Change to core directory and run migrations
cd core
echo Running migrations...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo Error: Failed to run migrations.
    exit /b 1
)
echo Migrations completed!

cd ..

echo.
echo ============================================================
echo Setup completed successfully!
echo ============================================================
echo.
echo Next steps:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Create a superuser: python manage.py createsuperuser
echo 3. Run the server: python manage.py runserver
echo.
echo Access the application at: http://127.0.0.1:8000
echo Fake admin (honeypot): http://127.0.0.1:8000/admin/login
echo Real admin: http://127.0.0.1:8000/secret-admin-entrance/
echo.

