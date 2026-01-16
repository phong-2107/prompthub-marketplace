# 📂 Project Structure - PromptHub Digital Marketplace

## Overview
Professional Django project with PostgreSQL database and Digital Marketplace frontend.

---

## 🗂️ Directory Structure

```
PromptProject/
│
├── 📁 apps/                          # Django Applications
│   ├── core/                         # Core functionality
│   │   ├── views.py                  # ✅ home() renders marketplace/home.html
│   │   ├── urls.py                   # Main routing ('' → home view)
│   │   └── ...
│   ├── prompthub/                    # Prompt marketplace app
│   │   ├── models.py                 # Prompt, Category, Review models
│   │   └── ...
│   ├── users/                        # User management
│   ├── api/                          # REST API
│   └── ...
│
├── 📁 templates/                     # Django Templates
│   ├── marketplace/                  # ⭐ ACTIVE TEMPLATES (Home Page)
│   │   ├── base.html                 # Master layout template
│   │   ├── home.html                 # ✅ HOMEPAGE (extends base.html)
│   │   ├── partials/                 # Reusable components
│   │   │   ├── header.html           # Navigation menu
│   │   │   ├── footer.html           # Site footer
│   │   │   ├── mobile_menu.html      # Mobile navigation
│   │   │   ├── preloader.html        # Loading animation
│   │   │   ├── overlay.html          # Modal overlays
│   │   │   ├── scroll_top.html       # Scroll to top button
│   │   │   └── scripts.html          # JavaScript includes
│   │   └── sections/                 # Homepage sections
│   │       ├── banner.html           # Hero section with search
│   │       ├── brand.html            # Brand logos
│   │       ├── popular_items.html    # Popular products
│   │       ├── selling_products.html # Best sellers
│   │       ├── service.html          # Features/services
│   │       ├── arrival_products.html # New arrivals
│   │       ├── pricing.html          # Pricing plans
│   │       ├── featured_contributors.html
│   │       ├── become_seller.html
│   │       ├── testimonial.html
│   │       ├── article.html          # Blog/articles
│   │       ├── newsletter.html       # Newsletter signup
│   │       └── resource.html         # Resources section
│   └── core/                         # Other core templates
│       └── about.html
│
├── 📁 assets/                        # ⭐ STATIC ASSETS (Frontend)
│   ├── css/                          # Stylesheets
│   │   ├── main.css                  # Main stylesheet
│   │   ├── bootstrap.min.css         # Bootstrap 5
│   │   └── ...
│   ├── js/                           # JavaScript files
│   │   ├── main.js                   # Main scripts
│   │   ├── jquery-3.7.1.min.js       # jQuery
│   │   ├── slick.min.js              # Slick carousel
│   │   └── ...
│   ├── images/                       # Images
│   │   ├── logo/                     # Site logos
│   │   ├── thumbs/                   # Product thumbnails
│   │   ├── shapes/                   # Design elements
│   │   └── gradients/                # Gradient backgrounds
│   ├── fonts/                        # Custom fonts
│   └── webfonts/                     # Font Awesome
│
├── 📁 static/                        # Django static files (collected)
├── 📁 staticfiles/                   # Production static files
├── 📁 media/                         # User uploads
│
├── 📁 config/                        # Django Settings
│   ├── settings/
│   │   ├── base.py                   # ✅ STATICFILES_DIRS includes assets/
│   │   ├── development.py
│   │   ├── staging.py
│   │   └── production.py
│   ├── urls.py                       # Main URL configuration
│   └── wsgi.py
│
├── 📁 database/                      # Database scripts
│   └── init.sql                      # PostgreSQL initialization
│
├── 📁 docker/                        # Docker configuration
│   ├── nginx/
│   └── entrypoint.sh
│
├── 📁 doc/                           # Documentation
│   ├── original_templates/           # 📦 ARCHIVED TEMPLATES
│   │   ├── index-two.html            # Original HTML file (10,383 lines)
│   │   └── partials-v2/              # Original partials (before conversion)
│   ├── PROJECT_GUIDE.md
│   └── CHEAT_SHEET.md
│
├── 📄 manage.py                      # Django management
├── 📄 docker-compose.yml             # Docker services
├── 📄 Dockerfile                     # Docker image
├── 📄 requirements.txt               # Python dependencies
├── 📄 .env                           # Environment variables
│
└── 📄 Documentation Files
    ├── README.md                     # Project overview
    ├── CONVERSION_COMPLETE.md        # Frontend conversion summary
    ├── FRONTEND_INTEGRATION.md       # Detailed integration guide
    ├── TEMPLATE_CONVERSION.md        # Conversion process
    └── PROJECT_STRUCTURE.md          # ⭐ THIS FILE

```

---

## 🎯 Key Components

### 1. Homepage Flow
```
User Request: http://localhost:8000/
    ↓
config/urls.py: '' → include('apps.core.urls')
    ↓
apps/core/urls.py: '' → views.home
    ↓
apps/core/views.py: home() → render('marketplace/home.html')
    ↓
templates/marketplace/home.html: extends base.html, includes 13 sections
    ↓
templates/marketplace/base.html: Full HTML structure with partials
    ↓
Browser displays: Digital Marketplace Homepage
```

### 2. Template Hierarchy
```
base.html (Master Template)
├── partials/header.html
├── partials/preloader.html
├── partials/overlay.html
├── partials/scroll_top.html
├── partials/mobile_menu.html
├── {% block content %}
│   └── home.html (Homepage)
│       ├── sections/banner.html
│       ├── sections/brand.html
│       ├── sections/popular_items.html
│       ├── sections/selling_products.html
│       ├── sections/service.html
│       ├── sections/arrival_products.html
│       ├── sections/pricing.html
│       ├── sections/featured_contributors.html
│       ├── sections/become_seller.html
│       ├── sections/testimonial.html
│       ├── sections/article.html
│       ├── sections/newsletter.html
│       └── sections/resource.html
├── partials/footer.html
└── partials/scripts.html
```

### 3. Static Files Flow
```
Development:
assets/css/main.css → {% static 'assets/css/main.css' %} → Browser

Production:
assets/ → python manage.py collectstatic → staticfiles/ → Nginx → Browser
```

---

## 📝 File Locations

### Current Active Templates (In Use)
| Purpose | Location |
|---------|----------|
| Homepage | `templates/marketplace/home.html` |
| Base Layout | `templates/marketplace/base.html` |
| Navigation | `templates/marketplace/partials/header.html` |
| Footer | `templates/marketplace/partials/footer.html` |
| Sections | `templates/marketplace/sections/*.html` |

### Archived Templates (Reference Only)
| File | Location |
|------|----------|
| Original HTML | `doc/original_templates/index-two.html` |
| Original Partials | `doc/original_templates/partials-v2/` |

### Static Assets
| Type | Location |
|------|----------|
| CSS | `assets/css/` |
| JavaScript | `assets/js/` |
| Images | `assets/images/` |
| Fonts | `assets/fonts/` & `assets/webfonts/` |

---

## 🚀 How to Run

### Development
```bash
# Start all services
docker-compose up -d

# View homepage
http://localhost:8000

# Admin panel
http://localhost:8000/admin
```

### Manual
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Collect static files
python manage.py collectstatic --noinput

# Run server
python manage.py runserver

# Visit
http://localhost:8000
```

---

## 🔄 Database Integration (Next Steps)

Currently templates are static. To make them dynamic:

### 1. Update Views
```python
# apps/core/views.py
from apps.prompthub.models import Prompt, Category

def home(request):
    context = {
        'popular_prompts': Prompt.objects.filter(
            is_active=True,
            featured=True
        ).order_by('-views')[:8],
        
        'categories': Category.objects.filter(
            is_active=True
        ),
    }
    return render(request, 'marketplace/home.html', context)
```

### 2. Update Templates
```django
{# templates/marketplace/sections/popular_items.html #}
{% for prompt in popular_prompts %}
<div class="popular-item-card">
    <img src="{{ prompt.thumbnail.url }}" alt="{{ prompt.title }}">
    <h6>{{ prompt.title }}</h6>
    <p>${{ prompt.price }}</p>
</div>
{% endfor %}
```

---

## 📊 Template Statistics

| Metric | Count |
|--------|-------|
| Total Templates | 24 files |
| Base Templates | 2 files |
| Partials | 9 files |
| Sections | 13 files |
| Static Assets | 464 files |
| Lines of Code | ~1,500 lines (from 10,383 original) |

---

## ✅ Current Status

- ✅ Templates: Converted to Django format
- ✅ Static Files: Configured and ready
- ✅ Homepage: Active at root URL
- ✅ Routing: Configured correctly
- ✅ Design: 100% preserved from original
- ⏳ Database: Ready for integration

---

## 📚 Documentation Files

1. **PROJECT_STRUCTURE.md** (This file) - Directory structure and file locations
2. **FRONTEND_INTEGRATION.md** - Detailed integration guide
3. **CONVERSION_COMPLETE.md** - Conversion summary
4. **TEMPLATE_CONVERSION.md** - Quick conversion guide
5. **PROJECT_GUIDE.md** - Full project documentation
6. **CHEAT_SHEET.md** - Quick commands reference

---

**Last Updated:** 2026-01-16  
**Version:** 1.0  
**Status:** ✅ Production Ready (Static Templates)
