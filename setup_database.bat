@echo off
REM =============================================
REM Script setup Database PromptHub - Windows
REM =============================================

echo.
echo ========================================
echo   SETUP DATABASE PROMPTHUB
echo ========================================
echo.

REM Check if virtual environment is activated
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python first.
    pause
    exit /b 1
)

REM Menu
echo Chon phuong thuc setup:
echo.
echo 1. Django Migrations (Khuyen nghi)
echo 2. Import SQL truc tiep
echo 3. Reset database va setup lai
echo.

set /p choice="Nhap lua chon (1-3): "

if "%choice%"=="1" goto django_migrations
if "%choice%"=="2" goto sql_import
if "%choice%"=="3" goto reset_db

echo [ERROR] Lua chon khong hop le!
pause
exit /b 1

:django_migrations
echo.
echo [INFO] Chay Django migrations...
echo.

REM Tao migrations
echo [STEP 1/4] Creating migrations...
python manage.py makemigrations prompthub

REM Kiem tra migrations
echo.
echo [STEP 2/4] Reviewing migrations...
python manage.py showmigrations prompthub

REM Apply migrations
echo.
echo [STEP 3/4] Applying migrations...
python manage.py migrate prompthub

REM Import seed data
echo.
set /p seed="Import du lieu mau? (y/n): "
if /i "%seed%"=="y" (
    echo [STEP 4/4] Importing seed data...
    python manage.py setup_prompthub_db --seed
) else (
    echo [STEP 4/4] Skipped seed data import
)

goto success

:sql_import
echo.
echo [INFO] Import SQL truc tiep...
echo.

REM Check if psql exists
psql --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] psql not found! Please install PostgreSQL client.
    pause
    exit /b 1
)

REM Get database credentials
set /p DB_NAME="Database name (default: prompthub): "
if "%DB_NAME%"=="" set DB_NAME=prompthub

set /p DB_USER="Database user (default: postgres): "
if "%DB_USER%"=="" set DB_USER=postgres

set /p DB_HOST="Database host (default: localhost): "
if "%DB_HOST%"=="" set DB_HOST=localhost

echo.
echo [STEP 1/3] Creating database...
createdb -U %DB_USER% -h %DB_HOST% %DB_NAME%

echo.
echo [STEP 2/3] Importing schema...
psql -U %DB_USER% -h %DB_HOST% -d %DB_NAME% -f "database\schema.sql"

echo.
set /p seed="Import du lieu mau? (y/n): "
if /i "%seed%"=="y" (
    echo [STEP 3/3] Importing seed data...
    psql -U %DB_USER% -h %DB_HOST% -d %DB_NAME% -f "database\seed_data.sql"
) else (
    echo [STEP 3/3] Skipped seed data import
)

echo.
echo [INFO] Dong bo Django voi database...
python manage.py migrate --fake-initial

goto success

:reset_db
echo.
echo [WARNING] CANH BAO: Thao tac nay se XOA TAT CA du lieu PromptHub!
echo.
set /p confirm="Ban co chac chan muon tiep tuc? (yes/no): "
if /i not "%confirm%"=="yes" (
    echo Huy thao tac.
    pause
    exit /b 0
)

echo.
echo [INFO] Resetting database...
python manage.py setup_prompthub_db --reset --seed

goto success

:success
echo.
echo ========================================
echo   SETUP HOAN THANH!
echo ========================================
echo.
echo Cac buoc tiep theo:
echo 1. Chay development server: python manage.py runserver
echo 2. Truy cap admin: http://localhost:8000/admin
echo 3. Xem database guide: DATABASE_GUIDE.md
echo.

pause
exit /b 0
