@echo off
echo ========================================
echo Odoo 18 Final Startup
echo ========================================
echo.

echo 1. Starting PostgreSQL...
net start postgresql-x64-17 2>nul
if errorlevel 1 (
    echo PostgreSQL is already running
)

echo 2. Activating virtual environment...
call venv\Scripts\activate.bat

echo 3. Starting Odoo...
cd odoo
python odoo-bin --config=..\odoo.conf

echo.
echo Access Odoo at: http://localhost:8069
echo Default master password: admin
echo.
pause