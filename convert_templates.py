"""
Script to convert partials-v2 HTML files to Django templates
Automatically converts static asset paths to use {% static %} tag
"""
import os
import re
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
PARTIALS_V2_SECTIONS = BASE_DIR / 'partials-v2' / 'sections'
TEMPLATES_SECTIONS = BASE_DIR / 'templates' / 'marketplace' / 'sections'

# Ensure templates directory exists
TEMPLATES_SECTIONS.mkdir(parents=True, exist_ok=True)

# Mapping of partial files to Django template names
SECTION_MAPPING = {
    '_BannerTwo.html': 'banner.html',
    '_BrandTwo.html': 'brand.html',
    '_PopularItemsTwo.html': 'popular_items.html',
    '_SellingProductsTwo.html': 'selling_products.html',
    '_ServiceTwo.html': 'service.html',
    '_ArrivalProductTwo.html': 'arrival_products.html',
    '_PricingTwo.html': 'pricing.html',
    '_FeaturedContributorTwo.html': 'featured_contributors.html',
    '_BecomeSellerTwo.html': 'become_seller.html',
    '_TestimonialTwo.html': 'testimonial.html',
    '_ArticleTwo.html': 'article.html',
    '_Newsletter.html': 'newsletter.html',
    '_ResourceTwo.html': 'resource.html',
}

def convert_static_paths(content):
    """
    Convert static asset paths to Django {% static %} template tags
    """
    # Add {% load static %} at the beginning if not present
    if '{% load static %}' not in content:
        content = '{% load static %}\n' + content
    
    # Convert href="assets/... to href="{% static 'assets/... %}"
    content = re.sub(
        r'href="(assets/[^"]+)"',
        r'href="{% static \'\1\' %}"',
        content
    )
    
    # Convert src="assets/... to src="{% static 'assets/... %}"
    content = re.sub(
        r'src="(assets/[^"]+)"',
        r'src="{% static \'\1\' %}"',
        content
    )
    
    # Convert href="index.html" or href="index-two.html" to {% url 'core:home' %}
    content = re.sub(
        r'href="index(-two|-three)?\.html"',
        r'href="{% url \'core:home\' %}"',
        content
    )
    
    # Convert common page links (we'll keep them as # for now, to be updated later)
    page_patterns = {
        r'href="all-product\.html"': 'href="#"  {# TODO: Update with products URL #}',
        r'href="product-details\.html"': 'href="#"  {# TODO: Update with product detail URL #}',
        r'href="profile\.html"': 'href="#"  {# TODO: Update with profile URL #}',
        r'href="cart\.html"': 'href="#"  {# TODO: Update with cart URL #}',
        r'href="dashboard\.html"': 'href="{% url \'admin:index\' %}"',
        r'href="login\.html"': 'href="{% url \'admin:login\' %}"',
        r'href="register\.html"': 'href="#"  {# TODO: Update with register URL #}',
        r'href="blog\.html"': 'href="#"  {# TODO: Update with blog URL #}',
        r'href="contact\.html"': 'href="{% url \'core:about\' %}"',
    }
    
    for pattern, replacement in page_patterns.items():
        content = re.sub(pattern, replacement, content)
    
    return content

def convert_section_file(source_file, dest_file):
    """
    Convert a single section file from partials-v2 to Django template
    """
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert static paths
        content = convert_static_paths(content)
        
        # Write to destination
        with open(dest_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'✓ Converted: {source_file.name} → {dest_file.name}')
        return True
    except Exception as e:
        print(f'✗ Error converting {source_file.name}: {e}')
        return False

def main():
    """
    Main conversion function
    """
    print('=' * 60)
    print('Converting partials-v2 sections to Django templates')
    print('=' * 60)
    print()
    
    success_count = 0
    total_count = len(SECTION_MAPPING)
    
    for source_name, dest_name in SECTION_MAPPING.items():
        source_file = PARTIALS_V2_SECTIONS / source_name
        dest_file = TEMPLATES_SECTIONS / dest_name
        
        if not source_file.exists():
            print(f'✗ Source file not found: {source_name}')
            continue
        
        if convert_section_file(source_file, dest_file):
            success_count += 1
    
    print()
    print('=' * 60)
    print(f'Conversion complete: {success_count}/{total_count} files converted')
    print('=' * 60)
    print()
    print('Next steps:')
    print('1. Review converted templates in templates/marketplace/sections/')
    print('2. Update TODO comments with actual URLs')
    print('3. Test the templates in your Django application')
    print('4. Connect templates to database models for dynamic content')

if __name__ == '__main__':
    main()
