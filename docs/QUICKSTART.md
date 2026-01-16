# 🚀 HƯỚNG DẪN CHẠY DỰ ÁN

## Tổng quan
PromptHub - Digital Marketplace với Django + PostgreSQL + Docker

---

## ⚡ Phương pháp 1: Chạy với Docker (Khuyến nghị)

### Yêu cầu
- Docker Desktop đã cài đặt
- Docker Compose đã cài đặt

### Các bước

#### 1. Khởi động tất cả services
```bash
docker-compose up -d
```

Lệnh này sẽ start:
- ✅ PostgreSQL database (port 5432)
- ✅ Redis cache (port 6379)
- ✅ Django web app (port 8000)
- ✅ Nginx web server (port 80)
- ✅ Celery worker
- ✅ Celery beat scheduler

#### 2. Kiểm tra trạng thái containers
```bash
docker-compose ps
```

Kết quả mong đợi:
```
NAME                  STATUS
django_db             Up (healthy)
django_redis          Up (healthy)
django_web            Up
django_nginx          Up
django_celery         Up
django_celery_beat    Up
```

#### 3. Xem logs (nếu cần debug)
```bash
# Xem tất cả logs
docker-compose logs

# Xem logs của web container
docker-compose logs -f web

# Xem logs của database
docker-compose logs -f db
```

#### 4. Truy cập website
```
🌐 Homepage:    http://localhost:8000/
🌐 Via Nginx:   http://localhost/
🔐 Admin:       http://localhost:8000/admin
```

#### 5. Tạo superuser (lần đầu chạy)
```bash
docker-compose exec web python manage.py createsuperuser
```
Nhập thông tin:
- Username: admin
- Email: admin@example.com
- Password: [your-password]

#### 6. Dừng services
```bash
# Dừng tất cả
docker-compose down

# Dừng và xóa volumes (reset database)
docker-compose down -v
```

---

## 🔧 Phương pháp 2: Chạy Local (Development)

### Yêu cầu
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Các bước

#### 1. Tạo và activate virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

#### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

#### 3. Cấu hình database PostgreSQL

##### Mở PostgreSQL command line:
```bash
psql -U postgres
```

##### Tạo database và user:
```sql
CREATE DATABASE django_dev;
CREATE USER django_user WITH PASSWORD 'your_password';
ALTER ROLE django_user SET client_encoding TO 'utf8';
ALTER ROLE django_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE django_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE django_dev TO django_user;
\q
```

#### 4. Cấu hình environment variables

##### Copy file .env:
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

##### Sửa file .env:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://django_user:your_password@localhost:5432/django_dev
REDIS_URL=redis://localhost:6379/0
```

#### 5. Chạy migrations
```bash
python manage.py migrate
```

#### 6. Collect static files
```bash
python manage.py collectstatic --noinput
```

#### 7. Tạo superuser
```bash
python manage.py createsuperuser
```

#### 8. Chạy development server
```bash
python manage.py runserver
```

#### 9. Chạy Celery (terminal mới)
```bash
# Worker
celery -A config worker -l info

# Beat scheduler (terminal thứ 3)
celery -A config beat -l info
```

#### 10. Truy cập website
```
🌐 Homepage:  http://localhost:8000/
🔐 Admin:     http://localhost:8000/admin
```

---

## 📋 Lệnh thường dùng

### Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart specific service
docker-compose restart web

# View logs
docker-compose logs -f web

# Execute command in container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell

# Rebuild containers
docker-compose up -d --build

# Remove all containers and volumes
docker-compose down -v
```

### Django Management Commands

```bash
# Database
python manage.py migrate                    # Run migrations
python manage.py makemigrations            # Create new migrations
python manage.py showmigrations            # Show migration status
python manage.py dbshell                   # Open database shell

# User management
python manage.py createsuperuser           # Create admin user
python manage.py changepassword admin      # Change password

# Static files
python manage.py collectstatic --noinput   # Collect static files
python manage.py findstatic file.css       # Find static file location

# Testing
python manage.py test                      # Run all tests
python manage.py test apps.core            # Run specific app tests
python manage.py check                     # Check for issues

# Shell
python manage.py shell                     # Open Django shell
python manage.py shell_plus                # Enhanced shell (needs django-extensions)

# Development
python manage.py runserver                 # Start dev server
python manage.py runserver 0.0.0.0:8000   # Start on all interfaces
```

### Celery Commands

```bash
# Worker
celery -A config worker -l info            # Start worker
celery -A config worker -l debug           # Start with debug logging

# Beat scheduler
celery -A config beat -l info              # Start beat scheduler

# Monitoring
celery -A config inspect active            # Show active tasks
celery -A config inspect stats             # Show worker stats
celery -A config purge                     # Clear all tasks
```

---

## 🔍 Troubleshooting

### Problem: Port 8000 đã được sử dụng
```bash
# Windows - Tìm và kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Problem: Database connection error
```bash
# Kiểm tra PostgreSQL đang chạy
# Windows
services.msc

# Linux
sudo systemctl status postgresql

# Mac
brew services list
```

### Problem: Docker containers không start
```bash
# Xem logs chi tiết
docker-compose logs

# Rebuild containers
docker-compose down
docker-compose up -d --build

# Reset everything
docker-compose down -v
docker system prune -a
docker-compose up -d --build
```

### Problem: Static files không load
```bash
# Collect static files lại
python manage.py collectstatic --noinput

# Với Docker
docker-compose exec web python manage.py collectstatic --noinput
docker-compose restart nginx
```

### Problem: Template syntax error
```bash
# Chạy script fix templates
python fix_templates.py

# Kiểm tra template errors
python manage.py check

# Với Docker
docker-compose exec web python manage.py check
```

### Problem: Migration conflicts
```bash
# Xem trạng thái migrations
python manage.py showmigrations

# Fake migrations nếu cần
python manage.py migrate --fake app_name migration_name

# Reset migrations (cẩn thận - mất data!)
python manage.py migrate app_name zero
```

---

## 📊 Kiểm tra sau khi chạy

### 1. Homepage loads
```bash
curl http://localhost:8000/
# Kết quả: HTTP 200 OK
```

### 2. Admin panel
- Truy cập: http://localhost:8000/admin
- Login với superuser account
- Check các models có hiển thị

### 3. Static files
- Check CSS load: View source → tìm `main.css`
- Check JS load: View source → tìm `main.js`
- Check images load: Inspect → Network tab

### 4. Database connection
```bash
# Docker
docker-compose exec web python manage.py dbshell
\dt  # List tables
\q   # Quit

# Local
python manage.py dbshell
\dt
\q
```

### 5. Redis connection
```bash
# Docker
docker-compose exec redis redis-cli
PING  # Should return PONG
EXIT

# Local
redis-cli
PING
EXIT
```

---

## 🎯 URLs quan trọng

| URL | Mô tả |
|-----|-------|
| http://localhost:8000/ | Homepage (Digital Marketplace) |
| http://localhost:8000/admin | Admin panel |
| http://localhost:8000/api/ | REST API endpoints |
| http://localhost/ | Via Nginx (chỉ Docker) |
| http://localhost:5432 | PostgreSQL (internal) |
| http://localhost:6379 | Redis (internal) |

---

## 📚 Cấu trúc project

```
PromptProject/
├── apps/                    # Django applications
│   ├── core/               # Core app (homepage)
│   ├── prompthub/          # Marketplace app
│   └── users/              # User management
├── templates/marketplace/  # Homepage templates
│   ├── home.html          # Main homepage
│   ├── base.html          # Base template
│   ├── partials/          # Reusable components
│   └── sections/          # Homepage sections
├── assets/                # Static assets (CSS/JS/images)
├── config/                # Django settings
├── docker/                # Docker configuration
└── manage.py              # Django management
```

---

## 🔐 Default Credentials

### Superuser (cần tạo lần đầu)
```
Username: admin
Password: [your-password]
```

### Database (Development)
```
Host: localhost (hoặc db với Docker)
Port: 5432
Name: django_dev
User: postgres (hoặc django_user)
Pass: postgres (hoặc your_password)
```

### Redis
```
Host: localhost (hoặc redis với Docker)
Port: 6379
DB: 0
```

---

## 🎨 Features

### Homepage (http://localhost:8000/)
- ✅ Hero banner với search
- ✅ Popular products (tabs)
- ✅ Best sellers
- ✅ New arrivals
- ✅ Pricing plans
- ✅ Testimonials
- ✅ Blog articles
- ✅ Newsletter signup
- ✅ Dark/Light mode toggle
- ✅ Fully responsive

### Admin Panel (http://localhost:8000/admin)
- ✅ User management
- ✅ Prompt management
- ✅ Category management
- ✅ Order management
- ✅ Review management

---

## 🚀 Next Steps

### 1. Customize Content
- Sửa templates trong `templates/marketplace/sections/`
- Thêm custom CSS trong `assets/css/`
- Thêm custom JS trong `assets/js/`

### 2. Database Integration
- Update `apps/core/views.py` với database queries
- Update templates với Django template tags
- Create additional views/URLs

### 3. Add New Features
- User registration/login
- Product listing page
- Product detail page
- Shopping cart
- Checkout flow
- User dashboard

### 4. Deploy to Production
- Set `DEBUG=False`
- Configure proper `SECRET_KEY`
- Set up proper database
- Configure static files CDN
- Set up SSL certificate
- Configure domain name

---

## 📖 Documentation

| File | Description |
|------|-------------|
| [README.md](README.md) | Project overview |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Complete structure guide |
| [QUICKSTART.md](QUICKSTART.md) | **⭐ This file** - Quick start guide |
| [FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md) | Frontend integration details |
| [CONVERSION_COMPLETE.md](CONVERSION_COMPLETE.md) | Template conversion summary |
| [RESTRUCTURE_COMPLETE.md](RESTRUCTURE_COMPLETE.md) | Project restructure summary |

---

## 💡 Tips

1. **Development**: Luôn dùng Docker để tránh conflict dependencies
2. **Debug**: Set `DEBUG=True` và check logs thường xuyên
3. **Static files**: Chạy `collectstatic` sau mỗi lần sửa CSS/JS
4. **Database**: Backup database trước khi chạy migrations mới
5. **Git**: Commit thường xuyên, không commit `.env` file

---

## ✅ Quick Checklist

- [ ] Docker Desktop đang chạy
- [ ] Run `docker-compose up -d`
- [ ] Check `docker-compose ps` - all containers running
- [ ] Visit http://localhost:8000/ - homepage loads
- [ ] Create superuser với `docker-compose exec web python manage.py createsuperuser`
- [ ] Login admin at http://localhost:8000/admin
- [ ] Check static files load correctly
- [ ] Test responsive design on mobile

---

**Ready to start?** Run: `docker-compose up -d` 🚀

**Need help?** Check logs: `docker-compose logs -f web`

**Version:** 1.0  
**Last Updated:** 2026-01-16  
**Status:** ✅ Ready for Development
