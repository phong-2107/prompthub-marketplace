# PromptHub - Digital Marketplace

Professional Django web application for digital marketplace with PostgreSQL database and modern frontend.

---

## 🚀 QUICK START

**New to this project?** → Start here: **[START_HERE.md](START_HERE.md)** ⭐

```bash
# 1. Start project
docker-compose up -d

# 2. Create admin user
docker-compose exec web python manage.py createsuperuser

# 3. Visit
http://localhost:8000/
```

**Full guide:** [QUICKSTART.md](QUICKSTART.md) | **Commands:** [COMMANDS_CHEATSHEET.md](COMMANDS_CHEATSHEET.md)

---

## 📚 Documentation

### Quick Start Guides
| Guide | Description |
|-------|-------------|
| **[START_HERE.md](START_HERE.md)** | ⭐ **Start here** - Quick start in 3 steps |
| **[QUICKSTART.md](QUICKSTART.md)** | Complete setup guide with troubleshooting |
| **[COMMANDS_CHEATSHEET.md](COMMANDS_CHEATSHEET.md)** | Quick command reference |
| **[DOCS_INDEX.md](DOCS_INDEX.md)** | Complete documentation index |

### Technical Documentation
| Guide | Description |
|-------|-------------|
| **[docs/DATABASE_GUIDE.md](docs/DATABASE_GUIDE.md)** | PostgreSQL & Django ORM guide |
| **[docs/DASHBOARD_SYSTEM.md](docs/DASHBOARD_SYSTEM.md)** | Admin dashboard documentation |
| **[docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)** | Directory structure & architecture |
| **[docs/VISUAL_GUIDE.md](docs/VISUAL_GUIDE.md)** | Visual diagrams & flow charts |
| **[docs/ROADMAP.md](docs/ROADMAP.md)** | Development roadmap & timeline |

---

## 🚀 Features

- ✅ **Backend**: Django 4.2 with modular architecture
- ✅ **Database**: PostgreSQL with optimized ORM
- ✅ **Frontend**: Professional Digital Marketplace template with Bootstrap 5
- ✅ **API**: Django REST Framework
- ✅ **Task Queue**: Celery + Redis
- ✅ **Caching**: Redis cache backend
- ✅ **Authentication**: Token-based & Session auth
- ✅ **Custom User Model**: Extended with custom fields
- ✅ **Docker**: Complete containerization
- ✅ **Production Ready**: Gunicorn + Nginx
- ✅ **Responsive Design**: Mobile-first marketplace interface

## 📁 Project Structure

```
PromptProject/
├── apps/                           # Django applications
│   ├── core/                       # ✅ Core app (Homepage)
│   │   ├── views.py               # home() → marketplace/home.html
│   │   └── urls.py                # '' → home view
│   ├── prompthub/                  # Marketplace app
│   ├── users/                      # User management
│   └── api/                        # REST API
├── templates/                      # ✅ Django Templates
│   └── marketplace/                # ⭐ ACTIVE HOMEPAGE
│       ├── base.html              # Master template
│       ├── home.html              # Homepage (13 sections)
│       ├── partials/              # Reusable components (7 files)
│       └── sections/              # Homepage sections (13 files)
├── assets/                         # ✅ Frontend Assets
│   ├── css/                       # Stylesheets (Bootstrap, main.css)
│   ├── js/                        # JavaScript (jQuery, slick, etc.)
│   ├── images/                    # Images & graphics
│   ├── fonts/                     # Custom fonts
│   └── webfonts/                  # Font Awesome
├── config/                         # Django configuration
│   ├── settings/base.py           # ✅ STATICFILES_DIRS includes assets/
│   └── urls.py                    # Root routing
├── docker/                         # Docker configuration
├── docs/                           # 📚 Technical Documentation
│   ├── DATABASE_GUIDE.md          # Database guide
│   ├── DASHBOARD_SYSTEM.md        # Dashboard docs
│   ├── PROJECT_STRUCTURE.md       # Structure guide
│   ├── VISUAL_GUIDE.md            # Visual diagrams
│   └── ROADMAP.md                 # Development roadmap
├── doc/                            # Archived files
│   └── original_templates/        # Original HTML templates
├── static/                         # Django static files
└── media/                          # User uploads
├── templates/                      # HTML templates
│   ├── base.html                  # Base template
│   └── core/
│       ├── home.html              # Home page
│       └── about.html             # About page
├── media/                          # User uploads
├── .env.example                    # Environment variables example
├── .gitignore                      # Git ignore file
├── docker-compose.yml              # Docker Compose config
├── Dockerfile                      # Docker image
├── manage.py                       # Django management
├── requirements.txt                # Python dependencies
├── docker-compose.yml              # Docker services
└── README.md                       # This file
```

**📚 Full documentation:** See [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) for detailed structure

## 🏠 Homepage

The project uses a professional **Digital Marketplace** template as the homepage:

- **URL**: `http://localhost:8000/` → `marketplace/home.html`
- **Template**: 24 modular Django templates (base + partials + sections)
- **Features**: Hero banner, product listings, categories, pricing, testimonials, blog
- **Design**: Fully responsive with dark/light mode toggle
- **Assets**: Complete CSS/JS/images included in `assets/` folder

## 🔧 System Requirements

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (tùy chọn)

## 📦 Cài đặt

### Phương pháp 1: Cài đặt Local (Development)

#### 1. Clone repository

```bash
git clone <repository-url>
cd PromptProject
```

#### 2. Tạo virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

#### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

#### 4. Cấu hình PostgreSQL

Tạo database:

```sql
CREATE DATABASE django_dev;
CREATE USER postgres WITH PASSWORD 'postgres';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE django_dev TO postgres;
```

#### 5. Cấu hình environment variables

```bash
# Copy file .env.example thành .env
copy .env.example .env    # Windows
cp .env.example .env      # Linux/macOS

# Chỉnh sửa .env với thông tin của bạn
```

#### 6. Chạy migrations

```bash
python manage.py migrate
```

#### 7. Tạo superuser

```bash
python manage.py createsuperuser
```

#### 8. Collect static files

```bash
python manage.py collectstatic
```

#### 9. Chạy development server

```bash
python manage.py runserver
```

Truy cập: http://localhost:8000

#### 10. Chạy Celery (Terminal riêng)

```bash
# Celery Worker
celery -A config worker -l info

# Celery Beat (Terminal khác)
celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### Phương pháp 2: Sử dụng Docker (Khuyến nghị)

#### 1. Copy environment file

```bash
copy .env.example .env    # Windows
cp .env.example .env      # Linux/macOS
```

#### 2. Build và chạy containers

```bash
docker-compose up -d --build
```

#### 3. Chạy migrations trong container

```bash
docker-compose exec web python manage.py migrate
```

#### 4. Tạo superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

#### 5. Truy cập ứng dụng

- **Web Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API**: http://localhost:8000/api/

#### 6. Xem logs

```bash
# Tất cả services
docker-compose logs -f

# Chỉ web service
docker-compose logs -f web

# Chỉ celery
docker-compose logs -f celery
```

#### 7. Dừng containers

```bash
docker-compose down

# Xóa volumes (database data)
docker-compose down -v
```

## 📊 PromptHub Database

Dự án bao gồm database **PromptHub** - hệ thống quản lý Prompt AI chuyên nghiệp với đầy đủ tính năng:

- ✅ Quản lý người dùng & RBAC (Role-Based Access Control)
- ✅ AI Platforms & Models (ChatGPT, Claude, Gemini...)
- ✅ Quản lý Prompts với phân loại chi tiết
- ✅ Tương tác người dùng (Like, Save, Comment, Rating)
- ✅ Subscription & Payment system
- ✅ System config & Activity logging

### Setup Database Nhanh

**Với Docker (Khuyến nghị):**

```bash
# 1. Copy file .env cho Docker
copy .env.docker .env

# 2. Khởi động database
docker-compose up -d db redis

# 3. Chạy migrations
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# 4. Import dữ liệu mẫu
docker-compose exec web python manage.py setup_prompthub_db --seed
```

**Với Local:**

```bash
# Windows
setup_database.bat

# Linux/macOS
chmod +x setup_database.sh
./setup_database.sh
```

📖 **Xem hướng dẫn chi tiết**: 
- Docker: [DOCKER_DATABASE_SETUP.md](DOCKER_DATABASE_SETUP.md)
- Local: [DATABASE_GUIDE.md](DATABASE_GUIDE.md)

## 🎯 Sử dụng

### Admin Panel

1. Truy cập: http://localhost:8000/admin
2. Đăng nhập với superuser đã tạo
3. Quản lý users, models, và data

### REST API

#### Authentication

**Login và lấy token:**

```bash
POST /api/auth/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}

Response:
{
  "token": "your-auth-token"
}
```

#### User Endpoints

**Lấy danh sách users:**

```bash
GET /api/users/
Authorization: Token your-auth-token
```

**Lấy profile hiện tại:**

```bash
GET /api/users/me/
Authorization: Token your-auth-token
```

**Tạo user mới:**

```bash
POST /api/users/
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepass123",
  "password_confirm": "securepass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Cập nhật profile:**

```bash
PUT /api/users/update_profile/
Authorization: Token your-auth-token
Content-Type: application/json

{
  "first_name": "Updated",
  "last_name": "Name",
  "bio": "My bio"
}
```

### Celery Tasks

Tạo custom task trong `apps/api/tasks.py`:

```python
from celery import shared_task

@shared_task
def send_email_task(email):
    # Send email logic
    return f"Email sent to {email}"
```

Sử dụng task:

```python
from apps.api.tasks import send_email_task

# Gọi async
result = send_email_task.delay('user@example.com')

# Hoặc gọi ngay lập tức
result = send_email_task('user@example.com')
```

## 🧪 Testing

Chạy tests:

```bash
# Tất cả tests
python manage.py test

# Test specific app
python manage.py test apps.users

# With coverage
coverage run --source='.' manage.py test
coverage report
```

## 🚀 Triển khai Production

### 1. Chuẩn bị môi trường

```bash
# Update .env file với production settings
DJANGO_SETTINGS_MODULE=config.settings.production
DEBUG=False
SECRET_KEY=<generate-strong-secret-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_PASSWORD=<strong-database-password>
```

### 2. Sử dụng Docker Compose

```bash
# Build production images
docker-compose -f docker-compose.yml up -d --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### 3. Cấu hình Nginx (nếu không dùng Docker)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/staticfiles/;
    }

    location /media/ {
        alias /path/to/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 4. Chạy Gunicorn

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

### 5. Setup SSL với Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### 6. Monitoring & Logging

```bash
# Xem logs
docker-compose logs -f web

# Database backup
docker-compose exec db pg_dump -U postgres django_dev > backup.sql

# Database restore
docker-compose exec -T db psql -U postgres django_dev < backup.sql
```

## 🔒 Bảo mật

### Checklist Production

- ✅ Set `DEBUG=False`
- ✅ Sử dụng strong `SECRET_KEY`
- ✅ Cấu hình `ALLOWED_HOSTS` đúng
- ✅ Enable HTTPS
- ✅ Set secure cookies (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`)
- ✅ Cấu hình CORS đúng
- ✅ Sử dụng environment variables cho sensitive data
- ✅ Regular security updates
- ✅ Database backups
- ✅ Rate limiting cho API

## 📚 Tài liệu tham khảo

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Tác giả

Dự án được xây dựng bởi Senior Full-Stack Developer

## 📧 Liên hệ

- Email: your-email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)

---

**Lưu ý**: Đây là template dự án. Hãy tùy chỉnh theo nhu cầu cụ thể của bạn.
