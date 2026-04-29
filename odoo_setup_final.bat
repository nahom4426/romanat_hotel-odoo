@echo off
echo Odoo 18 Final Setup
echo ====================
echo.

echo 1. Starting PostgreSQL...
net start postgresql-x64-17 2>nul
if errorlevel 1 (
    echo PostgreSQL is already running
)

echo 2. Activating virtual environment...
call venv\Scripts\activate.bat

echo 3. Recreating database...
python recreate_db.py
if errorlevel 1 (
    echo Failed to recreate database
    pause
    exit /b 1
)

echo 4. Initializing Odoo database...
cd odoo
python odoo-bin --addons-path=addons --db_host=localhost --db_port=5432 --db_user=odoo --db_password=odoo --database=odoo18 -i base --stop-after-init --without-demo=all
if errorlevel 1 (
    echo Failed to initialize database
    pause
    exit /b 1
)

echo 5. Starting Odoo...
python odoo-bin --addons-path=addons --db_host=localhost --db_port=5432 --db_user=odoo --db_password=odoo --database=odoo18 --without-demo=all

echo.
pause