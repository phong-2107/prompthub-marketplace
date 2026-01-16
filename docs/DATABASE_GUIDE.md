# 🗄️ HƯỚNG DẪN SỬ DỤNG DATABASE VỚI DJANGO

## 📋 MỤC LỤC
1. [Nguyên lý hoạt động](#nguyên-lý)
2. [Xem dữ liệu trong Database](#xem-dữ-liệu)
3. [Truy vấn dữ liệu trong Views](#truy-vấn-dữ-liệu)
4. [Hiển thị dữ liệu trong Templates](#hiển-thị-trong-templates)
5. [Ví dụ thực tế](#ví-dụ-thực-tế)

---

## 🎯 NGUYÊN LÝ HOẠT ĐỘNG

### Kiến trúc MTV (Model-Template-View)

```
┌─────────────────────────────────────────────────────┐
│                   Browser (Client)                   │
└─────────────────────┬───────────────────────────────┘
                      │ HTTP Request
                      ▼
┌─────────────────────────────────────────────────────┐
│              Django URL Routing                      │
│              urls.py → view function                 │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│                   VIEW (Logic)                       │
│  - Nhận request                                     │
│  - Truy vấn database qua Model                      │
│  - Xử lý business logic                             │
│  - Truyền data cho Template                         │
└─────────────────────┬───────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
┌────────────────┐         ┌──────────────────┐
│  MODEL (ORM)   │         │  TEMPLATE (HTML) │
│  - Query DB    │         │  - Nhận context  │
│  - Save data   │◄────────┤  - Render HTML   │
│  - Validation  │         │  - Template tags │
└────────┬───────┘         └──────────────────┘
         │
         ▼
┌─────────────────┐
│   PostgreSQL    │
│    Database     │
└─────────────────┘
```

### Django ORM (Object-Relational Mapping)

**Vai trò:** Chuyển đổi Python code thành SQL queries

```python
# Python Code (ORM)
prompts = Prompt.objects.filter(status='published')

# SQL tương đương
SELECT * FROM core_prompt WHERE status = 'published';
```

**Lợi ích:**
- ✅ Không cần viết SQL thủ công
- ✅ Bảo mật khỏi SQL Injection
- ✅ Type-safe với Python
- ✅ Database-agnostic (chuyển DB dễ dàng)

---

## 📊 PHẦN 1: XEM DỮ LIỆU TRONG DATABASE

### **Cách 1: Django Admin Panel** (Đơn giản nhất - Recommended)

#### Bước 1: Tạo superuser

```bash
docker-compose exec web python manage.py createsuperuser

# Nhập thông tin:
# Username: admin
# Email: admin@example.com
# Password: ******** (ít nhất 8 ký tự)
```

#### Bước 2: Truy cập Admin

```
URL: http://localhost:8000/admin/
Login: admin / password_bạn_vừa_tạo
```

#### Bước 3: Xem và quản lý data

- **Xem danh sách:** Click vào model (Categories, Prompts, Reviews...)
- **Tìm kiếm:** Dùng search box
- **Lọc:** Dùng filter sidebar bên phải
- **Thêm mới:** Click "Add ..."
- **Sửa:** Click vào record
- **Xóa:** Select records → Actions → Delete

**Ví dụ: Thêm Category mới**
```
1. Vào Admin → Categories → Add Category
2. Nhập:
   - Name: ChatGPT Prompts
   - Icon: fas fa-brain
   - Description: Prompts cho ChatGPT
3. Save → Slug tự động: chatgpt-prompts
```

---

### **Cách 2: Django Shell** (Cho Developers)

#### Mở Django Shell

```bash
docker-compose exec web python manage.py shell
```

#### Các lệnh cơ bản

```python
# Import models
from apps.core.models import Category, Prompt, Review
from django.contrib.auth import get_user_model
User = get_user_model()

# 1. Xem tất cả records
categories = Category.objects.all()
print(categories)  # <QuerySet [<Category: ChatGPT Prompts>, ...]>

# 2. Đếm số lượng
Category.objects.count()  # 5

# 3. Lấy 1 record
cat = Category.objects.get(slug='chatgpt-prompts')
print(cat.name)  # ChatGPT Prompts

# 4. Lọc records
published_prompts = Prompt.objects.filter(status='published')
featured = Prompt.objects.filter(featured=True)

# 5. Sắp xếp
newest = Prompt.objects.order_by('-created_at')[:10]  # 10 mới nhất

# 6. Query phức tạp
from django.db.models import Q
expensive = Prompt.objects.filter(price__gte=50)  # Giá >= $50
search = Prompt.objects.filter(
    Q(title__icontains='chatgpt') | Q(tags__icontains='ai')
)

# 7. Relationships
cat = Category.objects.get(id=1)
cat.prompts.all()  # Tất cả prompts thuộc category này

prompt = Prompt.objects.get(id=1)
prompt.category.name  # Tên category của prompt này
prompt.reviews.count()  # Số reviews

# 8. Aggregate
from django.db.models import Avg, Sum, Count
Prompt.objects.aggregate(
    avg_price=Avg('price'),
    total_views=Sum('views'),
    total_count=Count('id')
)

# 9. Tạo data mới
user = User.objects.first()
new_prompt = Prompt.objects.create(
    title="Test Prompt",
    description="Test description",
    content="Test content",
    category=cat,
    author=user,
    price=29.99,
    status='published'
)

# 10. Update
prompt = Prompt.objects.get(id=1)
prompt.views += 1
prompt.save()

# Hoặc bulk update
Prompt.objects.filter(status='draft').update(status='published')

# 11. Delete
Prompt.objects.get(id=99).delete()
```

**Thoát Shell:** `Ctrl+D` hoặc `exit()`

---

### **Cách 3: SQL Client Tools** (Cho Database Admins)

#### DBeaver (Free, Cross-platform)

```bash
# Connection Settings:
Host: localhost
Port: 5432
Database: django_db
Username: django_user
Password: django_password
```

#### pgAdmin (PostgreSQL Official)

```
1. Download: https://www.pgadmin.org/
2. Add Server:
   - Host: localhost
   - Port: 5432
   - Database: django_db
   - Username: django_user
```

#### SQL Queries trực tiếp

```sql
-- Xem tất cả categories
SELECT * FROM core_category;

-- Prompts được publish
SELECT id, title, price, status 
FROM core_prompt 
WHERE status = 'published';

-- Join với category
SELECT p.title, c.name as category, p.price
FROM core_prompt p
JOIN core_category c ON p.category_id = c.id;

-- Top 10 prompts có nhiều views nhất
SELECT title, views, downloads
FROM core_prompt
ORDER BY views DESC
LIMIT 10;
```

---

### **Cách 4: Django Management Command** (Tạo script riêng)

**Tạo file:** `apps/core/management/commands/show_stats.py`

```python
from django.core.management.base import BaseCommand
from apps.core.models import Prompt, Category

class Command(BaseCommand):
    help = 'Show database statistics'
    
    def handle(self, *args, **options):
        total_prompts = Prompt.objects.count()
        published = Prompt.objects.filter(status='published').count()
        categories = Category.objects.count()
        
        self.stdout.write(self.style.SUCCESS(f'''
        📊 Database Statistics:
        ----------------------
        Total Prompts: {total_prompts}
        Published: {published}
        Categories: {categories}
        '''))
```

**Chạy:**
```bash
docker-compose exec web python manage.py show_stats
```

---

## 🔍 PHẦN 2: TRUY VẤN DỮ LIỆU TRONG VIEWS

### Cấu trúc View Function

```python
# apps/core/views.py
from django.shortcuts import render, get_object_or_404
from .models import Prompt, Category

def home(request):
    """
    View hiển thị trang chủ
    
    Flow:
    1. Query data từ database
    2. Xử lý logic (filter, calculate...)
    3. Đóng gói data vào context dict
    4. Render template với context
    """
    
    # 1. Query data
    featured_prompts = Prompt.objects.filter(
        status='published',
        featured=True
    )[:8]  # Lấy 8 cái đầu
    
    trending = Prompt.objects.filter(
        status='published',
        is_trending=True
    )[:6]
    
    categories = Category.objects.all()
    
    # 2. Xử lý logic
    total_products = Prompt.objects.filter(status='published').count()
    
    # 3. Context dict
    context = {
        'featured_prompts': featured_prompts,
        'trending_prompts': trending,
        'categories': categories,
        'total_products': total_products,
    }
    
    # 4. Render
    return render(request, 'marketplace/home.html', context)
```

### Các Pattern Query phổ biến

```python
# 1. LIST VIEW - Danh sách sản phẩm
def prompt_list(request):
    # Get filter params từ URL
    category_slug = request.GET.get('category')
    search = request.GET.get('q')
    sort = request.GET.get('sort', '-created_at')
    
    # Base queryset
    prompts = Prompt.objects.filter(status='published')
    
    # Apply filters
    if category_slug:
        prompts = prompts.filter(category__slug=category_slug)
    
    if search:
        from django.db.models import Q
        prompts = prompts.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(tags__icontains=search)
        )
    
    # Sorting
    prompts = prompts.order_by(sort)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(prompts, 12)  # 12 items per page
    page = request.GET.get('page', 1)
    prompts_page = paginator.get_page(page)
    
    context = {
        'prompts': prompts_page,
        'categories': Category.objects.all(),
        'current_category': category_slug,
        'search_query': search,
    }
    
    return render(request, 'marketplace/prompt_list.html', context)


# 2. DETAIL VIEW - Chi tiết sản phẩm
def prompt_detail(request, slug):
    # get_object_or_404: Tự động return 404 nếu không tìm thấy
    prompt = get_object_or_404(
        Prompt.objects.select_related('category', 'author'),
        slug=slug,
        status='published'
    )
    
    # Tăng view count
    prompt.views += 1
    prompt.save(update_fields=['views'])
    
    # Related products
    related = Prompt.objects.filter(
        category=prompt.category,
        status='published'
    ).exclude(id=prompt.id)[:4]
    
    # Reviews
    reviews = prompt.reviews.select_related('user')[:10]
    
    context = {
        'prompt': prompt,
        'related_prompts': related,
        'reviews': reviews,
    }
    
    return render(request, 'marketplace/prompt_detail.html', context)


# 3. CATEGORY VIEW
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    
    prompts = Prompt.objects.filter(
        category=category,
        status='published'
    ).order_by('-created_at')
    
    # Stats
    stats = {
        'total': prompts.count(),
        'avg_price': prompts.aggregate(Avg('price'))['price__avg'],
    }
    
    context = {
        'category': category,
        'prompts': prompts,
        'stats': stats,
    }
    
    return render(request, 'marketplace/category.html', context)
```

### Performance Optimization

```python
# ❌ N+1 Query Problem (BAD)
def bad_view(request):
    prompts = Prompt.objects.all()
    # Template loop: {% for p in prompts %} {{ p.category.name }} {% endfor %}
    # → Chạy 1 query lấy prompts + N queries lấy category
    return render(request, 'template.html', {'prompts': prompts})


# ✅ Optimized với select_related (GOOD)
def good_view(request):
    prompts = Prompt.objects.select_related('category', 'author').all()
    # Chỉ 1 query với JOIN
    return render(request, 'template.html', {'prompts': prompts})


# ✅ prefetch_related cho many-to-many hoặc reverse FK
def view_with_reviews(request):
    prompts = Prompt.objects.prefetch_related('reviews').all()
    # 2 queries: 1 cho prompts, 1 cho tất cả reviews
    return render(request, 'template.html', {'prompts': prompts})
```

---

## 🎨 PHẦN 3: HIỂN THỊ DỮ LIỆU TRONG TEMPLATES

### Template Syntax Cơ Bản

```django
{# 1. Biến - {{ variable }} #}
<h1>{{ prompt.title }}</h1>
<p>Giá: ${{ prompt.price }}</p>

{# 2. If/Else #}
{% if prompt.is_on_sale %}
    <span class="badge">Sale {{ prompt.discount_percentage }}%</span>
{% else %}
    <span>Regular Price</span>
{% endif %}

{# 3. For Loop #}
{% for prompt in featured_prompts %}
    <div class="card">
        <h3>{{ prompt.title }}</h3>
        <p>{{ prompt.description|truncatewords:20 }}</p>
    </div>
{% empty %}
    <p>Không có sản phẩm nào.</p>
{% endfor %}

{# 4. Filters #}
{{ prompt.title|upper }}                {# CHỮ HOA #}
{{ prompt.description|truncatewords:15 }} {# Cắt 15 từ #}
{{ prompt.created_at|date:"d/m/Y" }}     {# 16/01/2026 #}
{{ prompt.price|floatformat:2 }}         {# 29.99 #}

{# 5. Template Tags #}
{% url 'prompt-detail' prompt.slug %}    {# /prompts/chatgpt-prompt/ #}
{% static 'assets/css/main.css' %}       {# /static/assets/css/main.css #}

{# 6. With #}
{% with total=prompts.count %}
    <p>Tìm thấy {{ total }} kết quả</p>
{% endwith %}

{# 7. Include #}
{% include 'partials/product_card.html' with prompt=item %}

{# 8. Block (inheritance) #}
{% extends 'base.html' %}
{% block content %}
    <h1>Nội dung trang</h1>
{% endblock %}
```

### Ví dụ: Product Card Component

**File:** `templates/marketplace/components/product_card.html`

```django
<div class="product-card">
    {# Thumbnail #}
    <div class="product-image">
        <img src="{{ prompt.thumbnail.url }}" alt="{{ prompt.title }}">
        
        {# Badges #}
        {% if prompt.featured %}
            <span class="badge badge-featured">Featured</span>
        {% endif %}
        
        {% if prompt.is_on_sale %}
            <span class="badge badge-sale">-{{ prompt.discount_percentage }}%</span>
        {% endif %}
    </div>
    
    {# Content #}
    <div class="product-content">
        {# Category #}
        <a href="{% url 'category-detail' prompt.category.slug %}" class="category-link">
            <i class="{{ prompt.category.icon }}"></i>
            {{ prompt.category.name }}
        </a>
        
        {# Title #}
        <h3>
            <a href="{% url 'prompt-detail' prompt.slug %}">
                {{ prompt.title }}
            </a>
        </h3>
        
        {# Description #}
        <p>{{ prompt.description|truncatewords:20 }}</p>
        
        {# Footer #}
        <div class="product-footer">
            {# Price #}
            <div class="price">
                {% if prompt.original_price %}
                    <span class="original">${{ prompt.original_price }}</span>
                {% endif %}
                <span class="current">${{ prompt.price }}</span>
            </div>
            
            {# Stats #}
            <div class="stats">
                <span><i class="las la-eye"></i> {{ prompt.views }}</span>
                <span><i class="las la-star"></i> {{ prompt.rating }}</span>
            </div>
        </div>
    </div>
</div>
```

### Ví dụ: Product List với Pagination

**File:** `templates/marketplace/prompt_list.html`

```django
{% extends 'marketplace/base.html' %}
{% load static %}

{% block content %}
<div class="container">
    {# Header #}
    <div class="page-header">
        <h1>
            {% if current_category %}
                {{ current_category.name }}
            {% else %}
                Tất cả Prompts
            {% endif %}
        </h1>
        <p>Tìm thấy {{ prompts.paginator.count }} kết quả</p>
    </div>
    
    {# Filters #}
    <div class="filters">
        <select name="sort" id="sort-select">
            <option value="-created_at">Mới nhất</option>
            <option value="price">Giá thấp → cao</option>
            <option value="-price">Giá cao → thấp</option>
            <option value="-views">Phổ biến nhất</option>
        </select>
    </div>
    
    {# Product Grid #}
    <div class="row">
        {% for prompt in prompts %}
            <div class="col-md-4 col-sm-6">
                {% include 'marketplace/components/product_card.html' %}
            </div>
        {% empty %}
            <div class="col-12">
                <p class="text-center">Không có sản phẩm nào.</p>
            </div>
        {% endfor %}
    </div>
    
    {# Pagination #}
    {% if prompts.has_other_pages %}
        <nav class="pagination">
            {% if prompts.has_previous %}
                <a href="?page=1">Đầu</a>
                <a href="?page={{ prompts.previous_page_number }}">Trước</a>
            {% endif %}
            
            <span class="current">
                Trang {{ prompts.number }} / {{ prompts.paginator.num_pages }}
            </span>
            
            {% if prompts.has_next %}
                <a href="?page={{ prompts.next_page_number }}">Sau</a>
                <a href="?page={{ prompts.paginator.num_pages }}">Cuối</a>
            {% endif %}
        </nav>
    {% endif %}
</div>
{% endblock %}
```

---

## 💡 VÍ DỤ THỰC TẾ: TRANG CHỦ DIGITAL MARKETPLACE

### Bước 1: Cập nhật View

**File:** `apps/core/views.py`

```python
from django.shortcuts import render
from django.db.models import Count
from .models import Prompt, Category


def home(request):
    """Trang chủ Digital Marketplace"""
    
    # Featured Prompts (8 items)
    featured = Prompt.objects.filter(
        status='published',
        featured=True
    ).select_related('category', 'author').order_by('-created_at')[:8]
    
    # Trending Prompts (6 items)
    trending = Prompt.objects.filter(
        status='published',
        is_trending=True
    ).select_related('category', 'author').order_by('-views')[:6]
    
    # Popular Categories (with product count)
    categories = Category.objects.annotate(
        product_count=Count('prompts', filter=Q(prompts__status='published'))
    ).order_by('-product_count')[:8]
    
    # New Arrivals (12 items)
    new_arrivals = Prompt.objects.filter(
        status='published'
    ).select_related('category', 'author').order_by('-created_at')[:12]
    
    # Stats
    from django.db.models import Sum
    stats = {
        'total_products': Prompt.objects.filter(status='published').count(),
        'total_downloads': Prompt.objects.aggregate(Sum('downloads'))['downloads__sum'] or 0,
        'total_categories': Category.objects.count(),
    }
    
    context = {
        'featured_prompts': featured,
        'trending_prompts': trending,
        'categories': categories,
        'new_arrivals': new_arrivals,
        'stats': stats,
    }
    
    return render(request, 'marketplace/home.html', context)
```

### Bước 2: Cập nhật Template

**File:** `templates/marketplace/sections/popular_prompts.html`

```django
<section class="popular-prompts py-5">
    <div class="container">
        <div class="section-header">
            <h2>Popular Prompts</h2>
            <a href="{% url 'prompt-list' %}" class="btn-view-all">View All</a>
        </div>
        
        <div class="row">
            {% for prompt in featured_prompts %}
                <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
                    <div class="prompt-card">
                        {# Image #}
                        <div class="card-image">
                            {% if prompt.thumbnail %}
                                <img src="{{ prompt.thumbnail.url }}" alt="{{ prompt.title }}">
                            {% else %}
                                <img src="{% static 'assets/images/placeholder.jpg' %}" alt="No image">
                            {% endif %}
                            
                            {# Overlay badges #}
                            <div class="card-badges">
                                {% if prompt.featured %}
                                    <span class="badge bg-warning">
                                        <i class="las la-star"></i> Featured
                                    </span>
                                {% endif %}
                                
                                {% if prompt.is_on_sale %}
                                    <span class="badge bg-danger">
                                        -{{ prompt.discount_percentage }}% OFF
                                    </span>
                                {% endif %}
                            </div>
                        </div>
                        
                        {# Content #}
                        <div class="card-body">
                            {# Category #}
                            <a href="{% url 'category-detail' prompt.category.slug %}" 
                               class="category-tag">
                                <i class="{{ prompt.category.icon }}"></i>
                                {{ prompt.category.name }}
                            </a>
                            
                            {# Title #}
                            <h4 class="card-title">
                                <a href="{% url 'prompt-detail' prompt.slug %}">
                                    {{ prompt.title|truncatewords:8 }}
                                </a>
                            </h4>
                            
                            {# Description #}
                            <p class="card-text">
                                {{ prompt.description|truncatewords:15 }}
                            </p>
                            
                            {# Footer #}
                            <div class="card-footer">
                                {# Author #}
                                <div class="author">
                                    <img src="{{ prompt.author.profile.avatar.url }}" 
                                         alt="{{ prompt.author.username }}"
                                         class="author-avatar">
                                    <span>{{ prompt.author.username }}</span>
                                </div>
                                
                                {# Price #}
                                <div class="price">
                                    {% if prompt.original_price %}
                                        <span class="old-price">
                                            ${{ prompt.original_price }}
                                        </span>
                                    {% endif %}
                                    <span class="current-price">
                                        ${{ prompt.price }}
                                    </span>
                                </div>
                            </div>
                            
                            {# Stats #}
                            <div class="card-stats">
                                <span title="Views">
                                    <i class="las la-eye"></i> {{ prompt.views }}
                                </span>
                                <span title="Downloads">
                                    <i class="las la-download"></i> {{ prompt.downloads }}
                                </span>
                                <span title="Rating">
                                    <i class="las la-star"></i> 
                                    {{ prompt.rating|floatformat:1 }}
                                    ({{ prompt.rating_count }})
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            {% empty %}
                <div class="col-12">
                    <div class="alert alert-info">
                        Chưa có sản phẩm nào. 
                        <a href="{% url 'admin:index' %}">Thêm sản phẩm mới</a>
                    </div>
                </div>
            {% endfor %}
        </div>
    </div>
</section>
```

### Bước 3: Cập nhật URLs

**File:** `apps/core/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('prompts/', views.prompt_list, name='prompt-list'),
    path('prompts/<slug:slug>/', views.prompt_detail, name='prompt-detail'),
    path('category/<slug:slug>/', views.category_detail, name='category-detail'),
]
```

---

## 🚀 CÁC BƯỚC THỰC HIỆN

### **BƯỚC 1: Tạo và Apply Migrations**

```bash
# Tạo migration files từ models
docker-compose exec web python manage.py makemigrations

# Xem SQL sẽ được execute
docker-compose exec web python manage.py sqlmigrate core 0001

# Apply migrations vào database
docker-compose exec web python manage.py migrate

# Kiểm tra migrations
docker-compose exec web python manage.py showmigrations
```

### **BƯỚC 2: Tạo Superuser**

```bash
docker-compose exec web python manage.py createsuperuser

# Username: admin
# Email: admin@promptmarket.com
# Password: Admin@123
```

### **BƯỚC 3: Thêm Dữ Liệu Mẫu**

#### Cách 1: Qua Admin Panel

```
1. Vào http://localhost:8000/admin/
2. Login với superuser
3. Add Categories:
   - ChatGPT Prompts (icon: fas fa-robot)
   - Midjourney Prompts (icon: fas fa-image)
   - Stable Diffusion (icon: fas fa-palette)
   - DALL-E Prompts (icon: fas fa-magic)

4. Add Prompts:
   - Title, description, content
   - Upload thumbnail image
   - Set price, category
   - Mark as featured/trending
   - Set status = published
```

#### Cách 2: Qua Django Shell

```bash
docker-compose exec web python manage.py shell
```

```python
from apps.core.models import Category, Prompt
from django.contrib.auth import get_user_model

User = get_user_model()
admin = User.objects.first()

# Tạo categories
categories_data = [
    {'name': 'ChatGPT Prompts', 'icon': 'fas fa-robot'},
    {'name': 'Midjourney', 'icon': 'fas fa-image'},
    {'name': 'Stable Diffusion', 'icon': 'fas fa-palette'},
    {'name': 'DALL-E', 'icon': 'fas fa-magic'},
]

for data in categories_data:
    Category.objects.get_or_create(
        name=data['name'],
        defaults={'icon': data['icon']}
    )

# Tạo prompts
cat_chatgpt = Category.objects.get(name='ChatGPT Prompts')

prompts_data = [
    {
        'title': 'Professional Email Writer',
        'description': 'Generate professional emails for any situation',
        'content': 'This prompt helps you write...',
        'price': 29.99,
        'original_price': 49.99,
    },
    {
        'title': 'Code Reviewer Assistant',
        'description': 'AI-powered code review and suggestions',
        'content': 'This prompt provides...',
        'price': 39.99,
        'featured': True,
    },
]

for data in prompts_data:
    Prompt.objects.create(
        category=cat_chatgpt,
        author=admin,
        status='published',
        **data
    )

print("✅ Created sample data!")
```

#### Cách 3: Management Command (Fixtures)

**Tạo file:** `apps/core/management/commands/seed_data.py`

```python
from django.core.management.base import BaseCommand
from apps.core.models import Category, Prompt
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Seed database with sample data'
    
    def handle(self, *args, **options):
        User = get_user_model()
        admin = User.objects.first()
        
        # Categories
        cat1, _ = Category.objects.get_or_create(
            name='ChatGPT Prompts',
            defaults={'icon': 'fas fa-robot'}
        )
        
        # Prompts
        for i in range(20):
            Prompt.objects.create(
                title=f'Sample Prompt {i+1}',
                description=f'This is sample prompt number {i+1}',
                content='Full content here...',
                category=cat1,
                author=admin,
                price=19.99 + i,
                status='published',
                featured=(i % 3 == 0),
            )
        
        self.stdout.write(self.style.SUCCESS('✅ Seeded 20 prompts!'))
```

**Chạy:**
```bash
docker-compose exec web python manage.py seed_data
```

### **BƯỚC 4: Test Query trong Shell**

```bash
docker-compose exec web python manage.py shell
```

```python
from apps.core.models import Prompt, Category

# Test queries
prompts = Prompt.objects.filter(status='published')
print(f"Published prompts: {prompts.count()}")

featured = Prompt.objects.filter(featured=True)
for p in featured:
    print(f"- {p.title} (${p.price})")

# Test relationships
cat = Category.objects.first()
print(f"Category: {cat.name}")
print(f"Prompts in this category: {cat.prompts.count()}")
```

### **BƯỚC 5: Update Views & Templates**

```bash
# Sao lưu file cũ
cp apps/core/views.py apps/core/views.py.backup

# Edit views.py với code ở trên
# Edit templates với code ở trên
```

### **BƯỚC 6: Restart Server & Test**

```bash
# Restart
docker-compose restart web

# Test homepage
curl http://localhost:8000/

# Check trong browser
# http://localhost:8000/
```

---

## 🎓 BEST PRACTICES

### 1. **Query Optimization**

```python
# ❌ BAD: N+1 queries
prompts = Prompt.objects.all()
for p in prompts:
    print(p.category.name)  # Query mỗi lần loop

# ✅ GOOD: 1 query với JOIN
prompts = Prompt.objects.select_related('category').all()
for p in prompts:
    print(p.category.name)  # Không query nữa
```

### 2. **Use select_related & prefetch_related**

```python
# select_related: ForeignKey, OneToOne (JOIN)
Prompt.objects.select_related('category', 'author')

# prefetch_related: ManyToMany, reverse FK (2 queries)
Prompt.objects.prefetch_related('reviews', 'purchases')

# Kết hợp
Prompt.objects.select_related('category').prefetch_related('reviews')
```

### 3. **Index Database Fields**

```python
class Prompt(models.Model):
    status = models.CharField(...)
    
    class Meta:
        indexes = [
            models.Index(fields=['status', '-created_at']),  # Composite index
            models.Index(fields=['featured']),
        ]
```

### 4. **Caching**

```python
from django.core.cache import cache

def home(request):
    featured = cache.get('featured_prompts')
    
    if not featured:
        featured = list(Prompt.objects.filter(featured=True)[:8])
        cache.set('featured_prompts', featured, 300)  # 5 minutes
    
    return render(request, 'home.html', {'featured': featured})
```

### 5. **Raw SQL khi cần**

```python
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT c.name, COUNT(p.id) as count
        FROM core_category c
        LEFT JOIN core_prompt p ON c.id = p.category_id
        GROUP BY c.id
    """)
    results = cursor.fetchall()
```

---

## 📝 CHECKLIST

- [ ] Models đã tạo xong (`models.py`)
- [ ] Admin đã register (`admin.py`)
- [ ] Migrations đã chạy (`makemigrations` + `migrate`)
- [ ] Superuser đã tạo
- [ ] Database có dữ liệu mẫu (qua admin hoặc shell)
- [ ] Views query đúng data
- [ ] Templates hiển thị data từ context
- [ ] URLs đã config đúng
- [ ] Server restart và test thành công

---

## 🆘 TROUBLESHOOTING

### Lỗi: No module named 'apps'

```python
# config/settings/base.py
INSTALLED_APPS = [
    ...
    'apps.core',  # ✅ Đúng
    # 'core',     # ❌ Sai
]
```

### Lỗi: Table doesn't exist

```bash
# Chạy migrations
docker-compose exec web python manage.py migrate
```

### Lỗi: FOREIGN KEY constraint failed

```python
# Phải tạo Category trước khi tạo Prompt
category = Category.objects.create(name='Test')
prompt = Prompt.objects.create(category=category, ...)
```

### Không thấy data trong template

```python
# Check view có pass data không
def my_view(request):
    data = Prompt.objects.all()
    print(f"Data count: {data.count()}")  # Debug
    return render(request, 'template.html', {'prompts': data})
```

```django
{# Check trong template #}
{{ prompts|length }}  {# Hiển thị số lượng #}
{{ prompts }}         {# Hiển thị QuerySet #}
```

---

## 📚 TÀI LIỆU THAM KHẢO

- Django QuerySet API: https://docs.djangoproject.com/en/4.2/ref/models/querysets/
- Template Language: https://docs.djangoproject.com/en/4.2/ref/templates/language/
- ORM Cookbook: https://books.agiliq.com/projects/django-orm-cookbook/

---

**Tạo bởi:** Senior Fullstack Developer
**Dự án:** Digital Marketplace - Django + PostgreSQL
**Ngày:** 16/01/2026
