# =============================================
# Setup Database PromptHub với Docker
# PowerShell Script cho Windows
# =============================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   SETUP DATABASE PROMPTHUB - DOCKER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Docker
Write-Host "[INFO] Checking Docker..." -ForegroundColor Yellow
$dockerInstalled = Get-Command docker -ErrorAction SilentlyContinue
if (-not $dockerInstalled) {
    Write-Host "[ERROR] Docker not found! Please install Docker Desktop first." -ForegroundColor Red
    Write-Host "Download: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "[OK] Docker found" -ForegroundColor Green

# Check docker-compose
$dockerComposeInstalled = Get-Command docker-compose -ErrorAction SilentlyContinue
if (-not $dockerComposeInstalled) {
    Write-Host "[ERROR] docker-compose not found!" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "[OK] docker-compose found" -ForegroundColor Green
Write-Host ""

# Step 1: Copy .env file
Write-Host "[STEP 1/6] Setting up environment file..." -ForegroundColor Cyan
if (Test-Path ".env") {
    $overwrite = Read-Host ".env already exists. Overwrite with Docker config? (y/n)"
    if ($overwrite -eq "y") {
        Copy-Item ".env.docker" ".env" -Force
        Write-Host "[OK] .env updated for Docker" -ForegroundColor Green
    } else {
        Write-Host "[SKIP] Using existing .env file" -ForegroundColor Yellow
        Write-Host "[WARNING] Make sure DB_HOST=db in your .env file!" -ForegroundColor Yellow
    }
} else {
    Copy-Item ".env.docker" ".env"
    Write-Host "[OK] .env created from .env.docker" -ForegroundColor Green
}
Write-Host ""

# Step 2: Start Database
Write-Host "[STEP 2/6] Starting PostgreSQL and Redis..." -ForegroundColor Cyan
docker-compose up -d db redis

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to start database containers" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "[OK] Database containers started" -ForegroundColor Green
Write-Host "[INFO] Waiting 15 seconds for database to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 15
Write-Host ""

# Step 3: Check containers
Write-Host "[STEP 3/6] Checking container status..." -ForegroundColor Cyan
docker-compose ps
Write-Host ""

# Step 4: Build web container
Write-Host "[STEP 4/6] Building web container..." -ForegroundColor Cyan
docker-compose build web

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to build web container" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "[OK] Web container built" -ForegroundColor Green
Write-Host ""

# Step 5: Run migrations
Write-Host "[STEP 5/6] Running database migrations..." -ForegroundColor Cyan

Write-Host "Creating migrations for prompthub..." -ForegroundColor Yellow
docker-compose run --rm web python manage.py makemigrations prompthub

Write-Host "Applying all migrations..." -ForegroundColor Yellow
docker-compose run --rm web python manage.py migrate

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Migrations failed" -ForegroundColor Red
    Write-Host "[TIP] Try: docker-compose run --rm web python manage.py showmigrations" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "[OK] Migrations completed" -ForegroundColor Green
Write-Host ""

# Step 6: Import seed data
Write-Host "[STEP 6/6] Importing seed data..." -ForegroundColor Cyan
$importSeed = Read-Host "Import sample data (roles, categories, AI platforms)? (y/n)"

if ($importSeed -eq "y") {
    docker-compose run --rm web python manage.py setup_prompthub_db --seed
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Seed data imported successfully" -ForegroundColor Green
    } else {
        Write-Host "[WARNING] Seed data import had issues" -ForegroundColor Yellow
    }
} else {
    Write-Host "[SKIP] Seed data import skipped" -ForegroundColor Yellow
}
Write-Host ""

# Create superuser
Write-Host "Creating superuser..." -ForegroundColor Cyan
$createSuperuser = Read-Host "Create Django superuser now? (y/n)"

if ($createSuperuser -eq "y") {
    docker-compose run --rm web python manage.py createsuperuser
} else {
    Write-Host "[SKIP] You can create superuser later with:" -ForegroundColor Yellow
    Write-Host "docker-compose exec web python manage.py createsuperuser" -ForegroundColor Yellow
}
Write-Host ""

# Start all services
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   SETUP COMPLETED!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$startServices = Read-Host "Start all services now? (y/n)"

if ($startServices -eq "y") {
    Write-Host "Starting all services..." -ForegroundColor Cyan
    docker-compose up -d
    
    Write-Host ""
    Write-Host "Services running at:" -ForegroundColor Green
    Write-Host "- Web Application: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "- Admin Panel:     http://localhost:8000/admin" -ForegroundColor Cyan
    Write-Host "- API:             http://localhost:8000/api/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "View logs with: docker-compose logs -f web" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "To start services later, run:" -ForegroundColor Yellow
    Write-Host "docker-compose up -d" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Yellow
Write-Host "- View logs:        docker-compose logs -f" -ForegroundColor Cyan
Write-Host "- Stop services:    docker-compose down" -ForegroundColor Cyan
Write-Host "- Restart web:      docker-compose restart web" -ForegroundColor Cyan
Write-Host "- Django shell:     docker-compose exec web python manage.py shell" -ForegroundColor Cyan
Write-Host "- Database shell:   docker-compose exec db psql -U postgres -d prompthub" -ForegroundColor Cyan
Write-Host ""
Write-Host "See DOCKER_DATABASE_SETUP.md for more details" -ForegroundColor Green
Write-Host ""

pause
