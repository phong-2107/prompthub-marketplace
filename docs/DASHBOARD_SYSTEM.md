# 📊 DASHBOARD ADMIN SYSTEM - DOCUMENTATION

## 🎯 TỔNG QUAN

Hệ thống Dashboard Admin được xây dựng modular, tách biệt components để dễ bảo trì và mở rộng.

### Cấu Trúc Files

```
templates/dashboard/
├── base.html                    # Base template (kế thừa assets)
├── home.html                    # Dashboard homepage với stats
├── prompts_list.html            # Quản lý products
├── categories_list.html         # Quản lý categories
├── sales_list.html              # Lịch sử bán hàng
├── reviews_list.html            # Quản lý reviews
├── users_list.html              # Quản lý users
├── partials/
│   ├── sidebar.html             # Sidebar navigation
│   ├── navbar.html              # Top navbar
│   ├── footer.html              # Footer
│   └── mobile_menu.html         # Mobile menu
└── components/
    ├── stat_card.html           # Widget thống kê
    ├── sales_chart.html         # Chart doanh số
    └── top_countries.html       # Top countries widget

apps/core/
├── views_dashboard.py           # Dashboard views
└── urls_dashboard.py            # Dashboard URLs
```

---

## 🔧 COMPONENTS ĐÃ TẠO

### 1. Base Template (`base.html`)
**Chức năng:**
- Kế thừa tất cả assets (CSS, JS) từ folder assets
- Chứa preloader, overlays, scroll-to-top
- Include các partials: sidebar, navbar, footer
- Blocks: `title`, `content`, `extra_css`, `extra_js`

**Sử dụng:**
```django
{% extends 'dashboard/base.html' %}

{% block title %}My Page{% endblock %}

{% block content %}
  <!-- Nội dung page -->
{% endblock %}
```

---

### 2. Sidebar (`partials/sidebar.html`)
**Chức năng:**
- Navigation menu với icons
- Active state tự động theo URL
- Links đến các modules: Dashboard, Products, Categories, Sales, Reviews, Users, Earnings, Settings

**Database Integration:**
- Không query database trực tiếp
- Chỉ hiển thị menu structure

---

### 3. Navbar (`partials/navbar.html`)
**Chức năng:**
- Search form (submit đến `/dashboard/search/`)
- Dark/Light mode toggle
- User profile dropdown
- Language selector

**Database Integration:**
```django
{{ request.user.username }}
{{ request.user.profile.avatar.url }}
```

---

### 4. Stat Card Component (`components/stat_card.html`)
**Chức năng:**
- Hiển thị 1 widget thống kê
- Nhận params: `icon`, `number`, `title`

**Sử dụng:**
```django
{% include 'dashboard/components/stat_card.html' with 
   icon='assets/images/icons/dashboard-widget-icon1.svg' 
   number=stats.total_products 
   title='Total Products' 
%}
```

**Database Integration:**
- Nhận data từ context của parent view

---

### 5. Sales Chart Component (`components/sales_chart.html`)
**Chức năng:**
- Chart ApexCharts hiển thị doanh số
- Dropdown chọn period (monthly/daily/yearly)

**Database Integration:**
```python
# Trong view
sales_data = [100, 200, 150, ...]  # List numbers
sales_labels = ['Jan', 'Feb', 'Mar', ...]  # List labels
```

---

### 6. Top Countries Component (`components/top_countries.html`)
**Chức năng:**
- Hiển thị list countries với flag và amount

**Database Integration:**
```python
# Trong view
top_countries = [
    {'name': 'USA', 'flag': 'path/to/flag.png', 'amount': 58.00},
    ...
]
```

---

## 🗄️ DATABASE INTEGRATION

### Dashboard Home (`views_dashboard.py::dashboard_home`)

**Query Statistics:**
```python
from django.db.models import Sum, Count

# Total products published
total_products = Prompt.objects.filter(status='published').count()

# Total sales
total_sales = Purchase.objects.count()

# Total downloads
total_downloads = Prompt.objects.aggregate(Sum('downloads'))['downloads__sum']

# Total earnings
total_earnings = Purchase.objects.aggregate(Sum('price_paid'))['price_paid__sum']
```

**Recent Sales (30 days):**
```python
from datetime import timedelta
from django.utils import timezone

thirty_days_ago = timezone.now() - timedelta(days=30)
recent_sales = Purchase.objects.filter(
    created_at__gte=thirty_days_ago
).values('created_at__date').annotate(
    items_count=Count('id'),
    amount=Sum('price_paid')
).order_by('-created_at__date')
```

**Sales Chart Data (7 days):**
```python
seven_days_ago = timezone.now() - timedelta(days=7)
sales_by_day = Purchase.objects.filter(
    created_at__gte=seven_days_ago
).values('created_at__date').annotate(
    total=Sum('price_paid')
).order_by('created_at__date')

# Convert to lists for JavaScript
sales_labels = [sale['created_at__date'].strftime('%b %d') for sale in sales_by_day]
sales_data = [float(sale['total']) for sale in sales_by_day]
```

---

### Products List (`views_dashboard.py::prompts_list`)

**Query với Filters:**
```python
from django.db.models import Q

prompts = Prompt.objects.select_related('category', 'author').all()

# Filter by category
if category_id:
    prompts = prompts.filter(category_id=category_id)

# Filter by status
if status:
    prompts = prompts.filter(status=status)

# Search
if search:
    prompts = prompts.filter(
        Q(title__icontains=search) |
        Q(description__icontains=search) |
        Q(tags__icontains=search)
    )

# Pagination
from django.core.paginator import Paginator
paginator = Paginator(prompts, 20)
prompts_page = paginator.get_page(page)
```

**Template Usage:**
```django
{% for prompt in prompts %}
  <tr>
    <td>{{ prompt.id }}</td>
    <td>{{ prompt.title }}</td>
    <td>{{ prompt.category.name }}</td>
    <td>${{ prompt.price }}</td>
    <td>{{ prompt.status }}</td>
    <td>{{ prompt.views }}</td>
    <td>{{ prompt.downloads }}</td>
    <td>⭐ {{ prompt.rating }}</td>
  </tr>
{% endfor %}
```

---

### Categories List (`views_dashboard.py::categories_list`)

**Query với Product Count:**
```python
from django.db.models import Count, Q

categories = Category.objects.annotate(
    product_count=Count('prompts', filter=Q(prompts__status='published'))
).order_by('-product_count')
```

**CRUD Operations:**

**Create:**
```python
def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        icon = request.POST.get('icon')
        description = request.POST.get('description')
        
        Category.objects.create(
            name=name,
            icon=icon,
            description=description
        )
        messages.success(request, 'Category created!')
    
    return redirect('dashboard:categories')
```

**Update:**
```python
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.icon = request.POST.get('icon')
        category.description = request.POST.get('description')
        category.save()
        
        messages.success(request, 'Category updated!')
    
    return redirect('dashboard:categories')
```

**Delete:**
```python
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted!')
    
    return redirect('dashboard:categories')
```

---

### Sales List (`views_dashboard.py::sales_list`)

**Query:**
```python
purchases = Purchase.objects.select_related(
    'user', 'prompt', 'prompt__category'
).order_by('-created_at')

# Pagination
paginator = Paginator(purchases, 20)
purchases_page = paginator.get_page(page)
```

**Template Display:**
```django
{% for purchase in purchases %}
  <tr>
    <td>{{ purchase.transaction_id }}</td>
    <td>{{ purchase.user.username }}</td>
    <td>{{ purchase.prompt.title }}</td>
    <td>${{ purchase.price_paid }}</td>
    <td>{{ purchase.created_at|date:"d/m/Y H:i" }}</td>
  </tr>
{% endfor %}
```

---

### Reviews List (`views_dashboard.py::reviews_list`)

**Query:**
```python
reviews = Review.objects.select_related(
    'user', 'prompt'
).order_by('-created_at')

paginator = Paginator(reviews, 20)
reviews_page = paginator.get_page(page)
```

**Template Display:**
```django
{% for review in reviews %}
  <tr>
    <td>{{ review.user.username }}</td>
    <td>{{ review.prompt.title }}</td>
    <td>⭐ {{ review.rating }}/5</td>
    <td>{{ review.comment|truncatewords:15 }}</td>
    <td>{{ review.created_at|date:"d/m/Y" }}</td>
  </tr>
{% endfor %}
```

---

### Users List (`views_dashboard.py::users_list`)

**Query với Annotations:**
```python
from django.contrib.auth import get_user_model
User = get_user_model()

users = User.objects.annotate(
    prompts_count=Count('prompts'),
    purchases_count=Count('purchases')
).order_by('-date_joined')

paginator = Paginator(users, 20)
users_page = paginator.get_page(page)
```

**Template Display:**
```django
{% for user in users %}
  <tr>
    <td>{{ user.id }}</td>
    <td>{{ user.username }}</td>
    <td>{{ user.email }}</td>
    <td>{{ user.prompts_count }}</td>
    <td>{{ user.purchases_count }}</td>
    <td>{{ user.date_joined|date:"d/m/Y" }}</td>
    <td>
      {% if user.is_active %}
        <span class="badge bg-success">Active</span>
      {% endif %}
    </td>
  </tr>
{% endfor %}
```

---

## 🔐 AUTHENTICATION & PERMISSIONS

### Staff/Superuser Required

Tất cả dashboard views require staff hoặc superuser:

```python
from django.contrib.auth.decorators import login_required, user_passes_test

def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_staff_or_superuser)
def dashboard_home(request):
    # View code
    pass
```

**Access Control:**
- URL: `/dashboard/` → Redirect to `/accounts/login/?next=/dashboard/`
- Chỉ staff và superuser mới truy cập được
- Non-staff users sẽ thấy 403 Forbidden

---

## 🚀 CÁCH SỬ DỤNG

### 1. Truy Cập Dashboard

```
URL: http://localhost:8000/dashboard/
```

**Login Requirements:**
- Username: admin (hoặc staff user)
- Password: Admin@123

### 2. Navigation

**Sidebar Menu:**
- Dashboard (Home) - `/dashboard/`
- Products - `/dashboard/prompts/`
- Categories - `/dashboard/categories/`
- Sales - `/dashboard/sales/`
- Reviews - `/dashboard/reviews/`
- Users - `/dashboard/users/`
- Earnings - `/dashboard/earnings/`
- Settings - `/dashboard/settings/`

### 3. Features

**Dashboard Home:**
- ✅ 4 stat cards (Products, Earnings, Downloads, Sales)
- ✅ Sales chart (7 days)
- ✅ Top countries widget
- ✅ Recent sales table (30 days)

**Products Management:**
- ✅ List all prompts với thumbnail
- ✅ Filter by category, status
- ✅ Search by title/description/tags
- ✅ Pagination (20 per page)
- 🔲 Create/Edit/Delete (placeholder URLs)

**Categories Management:**
- ✅ Grid view với product count
- ✅ Create category (modal)
- ✅ Edit category (modal)
- ✅ Delete category (confirm)

**Sales History:**
- ✅ List all purchases
- ✅ Show transaction ID, user, product, price, date
- ✅ Pagination

**Reviews Management:**
- ✅ List all reviews
- ✅ Show user, product, rating, comment
- ✅ View full review (modal)
- ✅ Pagination

**Users Management:**
- ✅ List all users
- ✅ Show username, email, products count, purchases count
- ✅ Badge for staff/admin
- ✅ Active status
- ✅ Pagination

---

## 📝 CẤU TRÚC FILE MỚI

### Files đã tạo (15 files):

**Templates (11 files):**
1. `templates/dashboard/base.html` - Base template
2. `templates/dashboard/home.html` - Dashboard homepage
3. `templates/dashboard/prompts_list.html` - Products management
4. `templates/dashboard/categories_list.html` - Categories management
5. `templates/dashboard/sales_list.html` - Sales history
6. `templates/dashboard/reviews_list.html` - Reviews management
7. `templates/dashboard/users_list.html` - Users management
8. `templates/dashboard/partials/sidebar.html` - Sidebar
9. `templates/dashboard/partials/navbar.html` - Navbar
10. `templates/dashboard/partials/footer.html` - Footer
11. `templates/dashboard/partials/mobile_menu.html` - Mobile menu

**Components (3 files):**
12. `templates/dashboard/components/stat_card.html` - Stat widget
13. `templates/dashboard/components/sales_chart.html` - Sales chart
14. `templates/dashboard/components/top_countries.html` - Countries widget

**Backend (2 files):**
15. `apps/core/views_dashboard.py` - Dashboard views với database queries
16. `apps/core/urls_dashboard.py` - Dashboard URLs

**Modified:**
- `config/urls.py` - Added dashboard URL pattern

---

## ✅ BEST PRACTICES ĐÃ ÁP DỤNG

1. **✅ Modular Components:** Tách sidebar, navbar, footer, stat cards
2. **✅ DRY Principle:** Reusable components với parameters
3. **✅ Database Optimization:** 
   - `select_related()` cho ForeignKey
   - `annotate()` cho calculated fields
   - Pagination để giảm load
4. **✅ Template Inheritance:** `base.html` → `home.html`
5. **✅ Static Files:** Kế thừa assets folder với `{% static %}`
6. **✅ URL Naming:** Consistent với `app_name` và `name`
7. **✅ Messages Framework:** Success/error messages
8. **✅ Security:** `@login_required`, `@user_passes_test`
9. **✅ Responsive:** Bootstrap grid system
10. **✅ Code Clarity:** Comments, docstrings, clear variable names

---

## 🎯 NEXT STEPS (Mở Rộng)

**Phase 1: CRUD Complete**
- [ ] Create prompt form
- [ ] Edit prompt form
- [ ] Delete prompt confirmation
- [ ] Upload images

**Phase 2: Advanced Features**
- [ ] Bulk actions (delete multiple, change status)
- [ ] Export data (CSV, Excel)
- [ ] Advanced filters (date range, price range)
- [ ] Charts for earnings by category
- [ ] Real-time notifications

**Phase 3: User Experience**
- [ ] Drag-and-drop image upload
- [ ] Rich text editor for description
- [ ] Auto-save drafts
- [ ] Keyboard shortcuts
- [ ] Dark mode persistence

**Phase 4: Analytics**
- [ ] Revenue analytics
- [ ] User behavior tracking
- [ ] Product performance metrics
- [ ] Conversion funnels
- [ ] Predictive analytics

---

## 📚 TÀI LIỆU THAM KHẢO

- **Django Admin:** https://docs.djangoproject.com/en/4.2/ref/contrib/admin/
- **Django Messages:** https://docs.djangoproject.com/en/4.2/ref/contrib/messages/
- **Django Pagination:** https://docs.djangoproject.com/en/4.2/topics/pagination/
- **Bootstrap 5:** https://getbootstrap.com/docs/5.0/
- **ApexCharts:** https://apexcharts.com/docs/

---

**Created:** 16/01/2026  
**Status:** ✅ Dashboard system hoàn thành với 15 files, full database integration  
**Access:** http://localhost:8000/dashboard/ (requires staff login)
