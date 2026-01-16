"""
Fix escaped quotes in Django templates.
Converts: {% static \'path\' %} → {% static 'path' %}
"""
import os
import re

TEMPLATES_DIR = 'templates/marketplace'

def fix_escaped_quotes(content):
    """Remove escaped quotes in {% static %} tags."""
    # Fix {% static \'path\' %} → {% static 'path' %}
    content = re.sub(r"\{% static \\'([^']+)\\' %\}", r"{% static '\1' %}", content)
    return content

def fix_template_file(filepath):
    """Fix a single template file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = fix_escaped_quotes(content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

def main():
    """Fix all template files."""
    print("=" * 60)
    print("Fixing escaped quotes in Django templates")
    print("=" * 60)
    print()
    
    fixed_count = 0
    total_count = 0
    
    # Fix all HTML files in templates/marketplace
    for root, dirs, files in os.walk(TEMPLATES_DIR):
        for filename in files:
            if filename.endswith('.html'):
                filepath = os.path.join(root, filename)
                total_count += 1
                
                if fix_template_file(filepath):
                    relative_path = os.path.relpath(filepath, TEMPLATES_DIR)
                    print(f"✓ Fixed: {relative_path}")
                    fixed_count += 1
    
    print()
    print("=" * 60)
    print(f"Fixed: {fixed_count}/{total_count} files")
    print("=" * 60)

if __name__ == '__main__':
    main()
