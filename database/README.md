# 📊 PromptHub Database - Tổng kết

## ✅ Đã hoàn thành

### 1. **Schema PostgreSQL** (`database/schema.sql`)
- Chuyển đổi hoàn chỉnh từ SQL Server sang PostgreSQL
- 30+ tables với chuẩn hóa 3NF
- Indexes, constraints và triggers
- JSONB fields cho dữ liệu linh hoạt
- Timezone-aware timestamps

### 2. **Django Models** (`apps/prompthub/models.py`)
- 20+ Django models tương ứng với schema
- Relationships (ForeignKey, ManyToMany)
- Custom properties và methods
- Choices cho enums
- Meta classes với db_table names

### 3. **Django Admin** (`apps/prompthub/admin.py`)
- Admin interface cho tất cả models
- Inline editing cho related objects
- Search, filters và ordering
- Fieldsets cho organization
- Custom list displays

### 4. **Management Commands**
- `setup_prompthub_db`: Tự động setup database
- Support flags: `--seed`, `--reset`
- Import dữ liệu mẫu tự động

### 5. **Scripts Tự động**
- `setup_database.bat` (Windows)
- `setup_database.sh` (Linux/macOS)
- Interactive menu
- Error handling

### 6. **Tài liệu**
- `DATABASE_GUIDE.md`: Hướng dẫn đầy đủ
- Code examples
- Troubleshooting
- Best practices

## 🚀 Cách sử dụng

### Setup Database (Khuyến nghị)

**Cách 1: Dùng script tự động**

```bash
# Windows
setup_database.bat

# Linux/macOS  
chmod +x setup_database.sh
./setup_database.sh
```

Chọn option 1 (Django Migrations) → Import seed data

**Cách 2: Thủ công**

```bash
# Kích hoạt virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# Tạo migrations
python manage.py makemigrations prompthub

# Apply migrations
python manage.py migrate

# Import seed data
python manage.py setup_prompthub_db --seed
```

### Kiểm tra Database

```bash
# Xem tables
python manage.py dbshell
\dt

# Test models
python manage.py shell
>>> from apps.prompthub.models import Prompt, Category
>>> Category.objects.all()
>>> Prompt.objects.count()
```

### Truy cập Admin

1. Tạo superuser (nếu chưa có):
```bash
python manage.py createsuperuser
```

2. Chạy server:
```bash
python manage.py runserver
```

3. Truy cập: http://localhost:8000/admin

4. Quản lý:
   - Prompts
   - Categories & Tags
   - AI Platforms & Models
   - Subscription Plans
   - Users & Roles

## 📁 Cấu trúc Files

```
PromptProject/
├── database/
│   ├── schema.sql              # PostgreSQL schema
│   ├── seed_data.sql           # Dữ liệu mẫu
│   └── README.md               # Database docs
│
├── apps/
│   └── prompthub/
│       ├── models.py           # 20+ Django models
│       ├── admin.py            # Admin configuration
│       ├── management/
│       │   └── commands/
│       │       └── setup_prompthub_db.py
│       └── migrations/         # Auto-generated
│
├── DATABASE_GUIDE.md           # Hướng dẫn chi tiết
├── setup_database.bat          # Windows setup script
└── setup_database.sh           # Linux/macOS setup script
```

## 💡 Use Cases

### Tạo Prompt mới

```python
from apps.prompthub.models import Prompt, PromptContent, PromptLevel
from apps.users.models import User

# Tạo prompt
prompt = Prompt.objects.create(
    id_prompt='PRM000000001',
    title='Prompt Marketing Facebook Ads',
    slug='prompt-marketing-facebook-ads',
    created_by=User.objects.first(),
    status=3,  # Published
    level=PromptLevel.objects.get(id_level=2)
)

# Thêm content
PromptContent.objects.create(
    prompt=prompt,
    prompt_text='Tạo nội dung quảng cáo Facebook cho [PRODUCT]...',
    usage_guide='Thay [PRODUCT] bằng sản phẩm của bạn'
)
```

### Query Prompts

```python
# Top prompts
top_prompts = Prompt.objects.filter(
    status=3,
    active=True
).order_by('-view_count')[:10]

# By category
from apps.prompthub.models import Category
category = Category.objects.get(category_code='marketing')
marketing_prompts = category.prompts.filter(status=3)

# Search
results = Prompt.objects.filter(
    title__icontains='marketing'
)
```

### User Interactions

```python
from apps.prompthub.models import UserPromptInteraction

# Save prompt
interaction, _ = UserPromptInteraction.objects.get_or_create(
    user=request.user,
    prompt=prompt
)
interaction.is_saved = True
interaction.save()

# Update statistics
prompt.save_count += 1
prompt.save()
```

## 🔧 Troubleshooting

### Lỗi: Table already exists

```bash
# Reset migrations
python manage.py migrate prompthub zero
python manage.py migrate prompthub
```

### Lỗi: No module named 'apps.prompthub'

```bash
# Kiểm tra app đã được thêm vào INSTALLED_APPS
# config/settings/base.py
INSTALLED_APPS = [
    ...
    'apps.prompthub',
]
```

### Lỗi connection refused

```bash
# Kiểm tra PostgreSQL đang chạy
# Windows: services.msc → PostgreSQL
# Docker: docker-compose ps
```

## 📚 Models chính

### Core Models
- `Prompt`: Prompt chính
- `PromptContent`: Nội dung chi tiết
- `Category`: Danh mục
- `Tag`: Tags
- `PromptLevel`: Cấp độ (Basic, Advanced, Premium...)

### AI Models
- `AIPlatform`: Nền tảng AI (ChatGPT, Claude...)
- `AIModel`: Model cụ thể (GPT-4, Claude 3.5...)

### User Management
- `Role`: Vai trò
- `Permission`: Quyền hạn
- `RolePermission`: Gán quyền cho vai trò

### Interactions
- `UserPromptInteraction`: Like, Save, View, Rating
- `Comment`: Bình luận
- `UserCollection`: Bộ sưu tập cá nhân

### Subscription
- `SubscriptionPlan`: Gói dịch vụ
- `Payment`: Thanh toán (tích hợp sau)

## 🎓 Best Practices

1. **Luôn dùng transactions** khi create/update nhiều objects
2. **Select_related/Prefetch_related** để tối ưu queries
3. **Index các fields** thường xuyên filter/search
4. **Validate data** trước khi save
5. **Backup database** trước khi migration quan trọng

## 📖 Tài liệu

- [DATABASE_GUIDE.md](DATABASE_GUIDE.md) - Hướng dẫn đầy đủ
- [README.md](README.md) - Dự án tổng quan
- [Django Models Documentation](https://docs.djangoproject.com/en/4.2/topics/db/models/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 🤝 Support

Nếu gặp vấn đề:
1. Đọc [DATABASE_GUIDE.md](DATABASE_GUIDE.md)
2. Check migrations: `python manage.py showmigrations`
3. Xem logs: `python manage.py runserver --verbosity 3`
4. Reset database: `python manage.py setup_prompthub_db --reset`

---

**Note**: Database schema đã được tối ưu hóa từ SQL Server sang PostgreSQL với các cải tiến về performance và Django compatibility.
