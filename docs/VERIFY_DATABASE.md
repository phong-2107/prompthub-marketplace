# 🚀 QUICK START - Xem Dữ Liệu Database

## ✅ HOÀN THÀNH
- [x] Models đã tạo (Category, Prompt, Review, Purchase)
- [x] Database migrations đã chạy
- [x] Dữ liệu mẫu đã thêm (6 categories, 10 prompts)
- [x] Views đã update để query database
- [x] Data đang được pass vào templates

## 🔍 CÁCH 1: DJANGO ADMIN PANEL (Dễ nhất)

### Bước 1: Đặt password cho superuser

```bash
docker-compose exec web python manage.py shell
```

Trong shell:
```python
from django.contrib.auth import get_user_model
User = get_user_model()
admin = User.objects.get(username='admin')
admin.set_password('Admin@123')  # Đặt password mới
admin.save()
print("✅ Password updated!")
exit()
```

### Bước 2: Login Admin

1. Mở browser: **http://localhost:8000/admin/**
2. Login:
   - Username: `admin`
   - Password: `Admin@123`

### Bước 3: Xem và quản lý data

**Xem Categories:**
- Click **Categories** → Thấy 6 danh mục
- ChatGPT Prompts, Midjourney, Stable Diffusion, DALL-E, Claude AI, Marketing

**Xem Prompts:**
- Click **Prompts** → Thấy 10 sản phẩm
- Professional Email Writer ($29.99)
- Code Review Assistant ($39.99)
- Photorealistic Portrait Master ($44.99)
- ...

**Filter và Search:**
- Sidebar phải: Filter by Status, Featured, Category
- Search box: Tìm theo title, description, tags

**Edit record:**
- Click vào title → Sửa nội dung
- Upload ảnh thumbnail (nếu có)
- Save

---

## 🔍 CÁCH 2: DJANGO SHELL (Cho Developers)

### Mở Shell

```bash
docker-compose exec web python manage.py shell
```

### Query Examples

```python
from apps.core.models import Category, Prompt, Review
from django.contrib.auth import get_user_model

# 1. Xem tất cả categories
categories = Category.objects.all()
for cat in categories:
    print(f"{cat.name} ({cat.product_count} prompts)")

# 2. Xem featured prompts
featured = Prompt.objects.filter(featured=True)
print(f"Featured prompts: {featured.count()}")
for p in featured:
    print(f"- {p.title} (${p.price})")

# 3. Xem prompts theo category
chatgpt_cat = Category.objects.get(name='ChatGPT Prompts')
prompts = chatgpt_cat.prompts.all()
print(f"\n{chatgpt_cat.name}:")
for p in prompts:
    print(f"- {p.title}")

# 4. Xem stats
from django.db.models import Avg, Sum
stats = Prompt.objects.aggregate(
    total=Count('id'),
    avg_price=Avg('price'),
    total_views=Sum('views')
)
print(f"\nStats: {stats}")

# 5. Xem trending
trending = Prompt.objects.filter(is_trending=True)
for p in trending:
    print(f"🔥 {p.title} - {p.views} views")

# 6. Tạo prompt mới (test)
user = User.objects.first()
cat = Category.objects.first()

new_prompt = Prompt.objects.create(
    title="Test Prompt",
    description="This is a test",
    content="Full content...",
    category=cat,
    author=user,
    price=19.99,
    status='published'
)
print(f"✅ Created: {new_prompt.title}")

# 7. Update prompt
prompt = Prompt.objects.get(id=1)
prompt.views += 100
prompt.save()
print(f"✅ Updated views: {prompt.views}")

# 8. Delete prompt (cẩn thận!)
# Prompt.objects.get(id=99).delete()

# Thoát shell
exit()
```

---

## 🔍 CÁCH 3: SQL QUERY TRỰC TIẾP

### Connect PostgreSQL

```bash
docker-compose exec db psql -U django_user -d django_db
```

### SQL Queries

```sql
-- Xem tất cả categories
SELECT * FROM core_category;

-- Đếm prompts
SELECT COUNT(*) FROM core_prompt;

-- Prompts với category
SELECT 
    p.title,
    c.name as category,
    p.price,
    p.views,
    p.featured
FROM core_prompt p
JOIN core_category c ON p.category_id = c.id
WHERE p.status = 'published'
ORDER BY p.views DESC;

-- Top 5 expensive prompts
SELECT title, price 
FROM core_prompt 
ORDER BY price DESC 
LIMIT 5;

-- Prompts by category
SELECT 
    c.name,
    COUNT(p.id) as total_prompts,
    AVG(p.price) as avg_price
FROM core_category c
LEFT JOIN core_prompt p ON c.id = p.category_id
GROUP BY c.id, c.name;

-- Thoát
\q
```

---

## 🎨 XEM DATA TRONG TEMPLATES

### Current Status

✅ **Views đã query database:**
- `featured_prompts`: 6 prompts featured
- `trending_prompts`: 4 prompts trending
- `categories`: 6 categories
- `new_arrivals`: 10 prompts mới nhất
- `best_sellers`: Prompts theo downloads

✅ **Data đã pass vào context**

❌ **Templates chưa hiển thị data** (cần update template để loop qua data)

### Test trong Browser

1. **Mở homepage:** http://localhost:8000/

2. **View Page Source** (Ctrl+U)
   - Tìm: `featured_prompts`
   - Thấy: `'featured_prompts': '<<queryset of core.Prompt>>'`
   - ✅ Nghĩa là data đã được pass vào template

3. **Debug Toolbar** (nếu bật)
   - Xem SQL queries
   - Xem context variables

### Update Template để hiển thị data

**Ví dụ: Update popular_prompts.html**

```django
{# File: templates/marketplace/sections/popular_prompts.html #}

<section class="popular-prompts">
    <div class="container">
        <h2>Popular Prompts</h2>
        
        <div class="row">
            {% for prompt in featured_prompts %}
                <div class="col-md-3">
                    <div class="card">
                        {# Title #}
                        <h4>{{ prompt.title }}</h4>
                        
                        {# Description #}
                        <p>{{ prompt.description|truncatewords:15 }}</p>
                        
                        {# Category #}
                        <span class="badge">
                            <i class="{{ prompt.category.icon }}"></i>
                            {{ prompt.category.name }}
                        </span>
                        
                        {# Price #}
                        <div class="price">
                            {% if prompt.original_price %}
                                <span class="old">${{ prompt.original_price }}</span>
                            {% endif %}
                            <span class="current">${{ prompt.price }}</span>
                        </div>
                        
                        {# Stats #}
                        <div class="stats">
                            <span>👁️ {{ prompt.views }}</span>
                            <span>⬇️ {{ prompt.downloads }}</span>
                            <span>⭐ {{ prompt.rating }}</span>
                        </div>
                        
                        {# Badges #}
                        {% if prompt.featured %}
                            <span class="badge-featured">Featured</span>
                        {% endif %}
                        
                        {% if prompt.is_on_sale %}
                            <span class="badge-sale">-{{ prompt.discount_percentage }}%</span>
                        {% endif %}
                    </div>
                </div>
            {% empty %}
                <p>Chưa có sản phẩm nào.</p>
            {% endfor %}
        </div>
    </div>
</section>
```

---

## 📊 VERIFY DATABASE

### Check data có trong database

```bash
# Count records
docker-compose exec web python manage.py shell -c "
from apps.core.models import *
print('Categories:', Category.objects.count())
print('Prompts:', Prompt.objects.count())
print('Published:', Prompt.objects.filter(status='published').count())
print('Featured:', Prompt.objects.filter(featured=True).count())
"
```

Expected output:
```
Categories: 6
Prompts: 10
Published: 10
Featured: 6
```

### Check views có query không

```bash
# Test view query
docker-compose exec web python manage.py shell -c "
from apps.core.views import home
from django.test import RequestFactory

request = RequestFactory().get('/')
response = home(request)
print('Status:', response.status_code)
"
```

---

## 🎯 NEXT STEPS

1. **[DONE] ✅ Database setup**
   - Models created
   - Migrations applied
   - Sample data seeded

2. **[DONE] ✅ Views query database**
   - Featured prompts
   - Categories
   - Trending items
   - Stats

3. **[TODO] ⬜ Update templates**
   - Loop through `featured_prompts`
   - Display real product cards
   - Show categories from database
   - Display stats

4. **[TODO] ⬜ Add images**
   - Upload product thumbnails
   - Configure MEDIA_URL
   - Use `{{ prompt.thumbnail.url }}`

5. **[TODO] ⬜ Create detail pages**
   - URL: `/prompts/<slug>/`
   - View: `prompt_detail()`
   - Template: `prompt_detail.html`

---

## 🔗 USEFUL LINKS

- **Homepage:** http://localhost:8000/
- **Admin Panel:** http://localhost:8000/admin/
- **Django Docs:** https://docs.djangoproject.com/en/4.2/

---

**Generated:** 16/01/2026
**Status:** Database ready, Views updated, Templates need update
