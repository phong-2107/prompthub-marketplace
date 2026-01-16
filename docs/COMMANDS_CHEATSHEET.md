# ⚡ CHEAT SHEET - Lệnh nhanh

## 🚀 Start/Stop Project

```bash
# Start tất cả
docker-compose up -d

# Stop tất cả
docker-compose down

# Restart web
docker-compose restart web

# Xem logs
docker-compose logs -f web
```

## 🌐 URLs

| URL | Mô tả |
|-----|-------|
| http://localhost:8000/ | Homepage |
| http://localhost:8000/admin | Admin panel |
| http://localhost:8000/dashboard/ | Dashboard admin (staff only) |
| http://localhost/ | Via Nginx |

## 👤 Tạo Admin User

```bash
docker-compose exec web python manage.py createsuperuser
```

## 🗄️ Database

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create migrations
docker-compose exec web python manage.py makemigrations

# Database shell
docker-compose exec web python manage.py dbshell
```

## 📦 Static Files

```bash
# Collect static
docker-compose exec web python manage.py collectstatic --noinput

# Restart nginx
docker-compose restart nginx
```

## 🧹 Cleanup

```bash
# Stop và xóa containers
docker-compose down

# Xóa kể cả volumes (reset DB)
docker-compose down -v

# Rebuild containers
docker-compose up -d --build
```

## 🔍 Debug

```bash
# Check Django
docker-compose exec web python manage.py check

# Django shell
docker-compose exec web python manage.py shell

# Container status
docker-compose ps

# All logs
docker-compose logs

# Specific service logs
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f redis
```

## 📝 Common Tasks

```bash
# Test homepage
curl http://localhost:8000/

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run tests
docker-compose exec web python manage.py test

# Show migrations
docker-compose exec web python manage.py showmigrations

# Flush database
docker-compose exec web python manage.py flush
```

## 🐛 Quick Fixes

```bash
# Port 8000 busy
docker-compose restart web

# Static files not loading
docker-compose exec web python manage.py collectstatic --noinput
docker-compose restart nginx

# Database connection error
docker-compose restart db
docker-compose restart web

# Template errors
python fix_templates.py
docker-compose restart web

# Complete reset
docker-compose down -v
docker-compose up -d --build
```

## 📁 File Locations

```
Homepage template:     templates/marketplace/home.html
Static assets:         assets/
Settings:             config/settings/base.py
Main URLs:            config/urls.py
Core views:           apps/core/views.py
```

## ⚙️ Environment

```bash
# Development
DEBUG=True in .env

# Production
DEBUG=False in .env
```

## 📊 Monitoring

```bash
# Container status
docker-compose ps

# Resource usage
docker stats

# Container logs (live)
docker-compose logs -f

# Django debug
docker-compose exec web python manage.py check --deploy
```

---

**Quick Start:** `docker-compose up -d` → http://localhost:8000/ 🚀

**Full Guide:** [QUICKSTART.md](QUICKSTART.md)
