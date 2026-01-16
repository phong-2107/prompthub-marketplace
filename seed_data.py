from apps.core.models import Category, Prompt
from django.contrib.auth import get_user_model

User = get_user_model()
admin = User.objects.first()

# Kiểm tra user
if not admin:
    print("❌ No users found! Create superuser first.")
    exit()

print(f"✅ Using user: {admin.username}")

# Tạo categories
categories_data = [
    {
        'name': 'ChatGPT Prompts',
        'icon': 'fas fa-robot',
        'description': 'Professional prompts for ChatGPT and GPT-4'
    },
    {
        'name': 'Midjourney',
        'icon': 'fas fa-image',
        'description': 'Creative prompts for Midjourney AI art'
    },
    {
        'name': 'Stable Diffusion',
        'icon': 'fas fa-palette',
        'description': 'High-quality prompts for Stable Diffusion'
    },
    {
        'name': 'DALL-E',
        'icon': 'fas fa-magic',
        'description': 'Innovative prompts for DALL-E image generation'
    },
    {
        'name': 'Claude AI',
        'icon': 'fas fa-brain',
        'description': 'Effective prompts for Claude AI assistant'
    },
    {
        'name': 'Marketing',
        'icon': 'fas fa-bullhorn',
        'description': 'Marketing and copywriting prompts'
    },
]

print("\n📁 Creating categories...")
for data in categories_data:
    cat, created = Category.objects.get_or_create(
        name=data['name'],
        defaults={
            'icon': data['icon'],
            'description': data['description']
        }
    )
    status = "✨ Created" if created else "✓ Exists"
    print(f"{status}: {cat.name}")

# Tạo prompts
cat_chatgpt = Category.objects.get(name='ChatGPT Prompts')
cat_midjourney = Category.objects.get(name='Midjourney')
cat_marketing = Category.objects.get(name='Marketing')

prompts_data = [
    # ChatGPT Prompts
    {
        'title': 'Professional Email Writer',
        'description': 'Generate professional, polished emails for any business situation. Perfect for client communication, internal memos, and formal correspondence.',
        'content': 'This comprehensive prompt helps you craft professional emails by analyzing tone, context, and recipient. It considers business etiquette, cultural nuances, and communication goals to produce emails that get results.',
        'category': cat_chatgpt,
        'price': 29.99,
        'original_price': 49.99,
        'status': 'published',
        'featured': True,
        'tags': 'email, business, professional, communication',
        'views': 1250,
        'downloads': 342,
        'rating': 4.8,
        'rating_count': 89,
    },
    {
        'title': 'Code Review Assistant',
        'description': 'AI-powered code review with best practices, security checks, and optimization suggestions.',
        'content': 'This prompt transforms ChatGPT into an expert code reviewer that analyzes your code for bugs, security vulnerabilities, performance issues, and suggests improvements following industry best practices.',
        'category': cat_chatgpt,
        'price': 39.99,
        'status': 'published',
        'featured': True,
        'is_trending': True,
        'tags': 'coding, development, review, best-practices',
        'views': 2100,
        'downloads': 567,
        'rating': 4.9,
        'rating_count': 142,
    },
    {
        'title': 'Content Strategy Expert',
        'description': 'Create comprehensive content strategies for blogs, social media, and marketing campaigns.',
        'content': 'Develop data-driven content strategies that align with your business goals. This prompt helps you plan editorial calendars, identify content gaps, and create engaging content that resonates with your target audience.',
        'category': cat_marketing,
        'price': 34.99,
        'status': 'published',
        'featured': True,
        'tags': 'content, marketing, strategy, social-media',
        'views': 890,
        'downloads': 234,
        'rating': 4.7,
        'rating_count': 67,
    },
    {
        'title': 'SEO Article Generator',
        'description': 'Generate SEO-optimized articles that rank high on search engines while providing value to readers.',
        'content': 'This prompt creates search engine optimized content that balances keyword usage with readability. It includes meta descriptions, header structures, and internal linking suggestions.',
        'category': cat_marketing,
        'price': 24.99,
        'original_price': 39.99,
        'status': 'published',
        'is_trending': True,
        'tags': 'seo, article, content, ranking',
        'views': 1678,
        'downloads': 445,
        'rating': 4.6,
        'rating_count': 112,
    },
    # Midjourney Prompts
    {
        'title': 'Photorealistic Portrait Master',
        'description': 'Create stunning photorealistic portraits with perfect lighting, composition, and detail.',
        'content': 'Master prompt for generating ultra-realistic human portraits in Midjourney. Includes camera settings, lighting techniques, and composition guidelines for professional-quality results.',
        'category': cat_midjourney,
        'price': 44.99,
        'status': 'published',
        'featured': True,
        'tags': 'portrait, photorealistic, midjourney, photography',
        'views': 3200,
        'downloads': 789,
        'rating': 4.9,
        'rating_count': 203,
    },
    {
        'title': 'Fantasy Landscape Generator',
        'description': 'Epic fantasy landscapes with magical elements, dramatic lighting, and otherworldly atmospheres.',
        'content': 'Create breathtaking fantasy scenes with this detailed Midjourney prompt. Perfect for book covers, game art, and creative projects requiring imaginative landscapes.',
        'category': cat_midjourney,
        'price': 34.99,
        'status': 'published',
        'is_trending': True,
        'tags': 'fantasy, landscape, creative, art',
        'views': 2456,
        'downloads': 612,
        'rating': 4.8,
        'rating_count': 156,
    },
    {
        'title': 'Product Photography Pro',
        'description': 'Professional product photos for e-commerce with perfect lighting and studio-quality backgrounds.',
        'content': 'Generate high-end product photography in Midjourney. Ideal for online stores, catalogs, and marketing materials. Includes lighting setups and background options.',
        'category': cat_midjourney,
        'price': 49.99,
        'status': 'published',
        'featured': True,
        'tags': 'product, photography, ecommerce, professional',
        'views': 1890,
        'downloads': 523,
        'rating': 4.7,
        'rating_count': 134,
    },
    # More varied prompts
    {
        'title': 'Social Media Caption Wizard',
        'description': 'Engaging social media captions that drive engagement and conversions.',
        'content': 'Generate compelling captions for Instagram, Facebook, Twitter, and LinkedIn. Includes hashtag strategies and call-to-action optimization.',
        'category': cat_marketing,
        'price': 19.99,
        'status': 'published',
        'is_trending': True,
        'tags': 'social-media, captions, engagement, marketing',
        'views': 1234,
        'downloads': 389,
        'rating': 4.5,
        'rating_count': 98,
    },
    {
        'title': 'Business Plan Creator',
        'description': 'Comprehensive business plans with financial projections, market analysis, and strategy.',
        'content': 'Create professional business plans that attract investors. Includes executive summary, market research, financial models, and growth strategies.',
        'category': cat_chatgpt,
        'price': 54.99,
        'status': 'published',
        'featured': True,
        'tags': 'business, planning, startup, strategy',
        'views': 945,
        'downloads': 267,
        'rating': 4.9,
        'rating_count': 78,
    },
    {
        'title': 'Resume Optimizer Pro',
        'description': 'ATS-friendly resumes that pass automated screening and impress recruiters.',
        'content': 'Optimize your resume for both ATS systems and human recruiters. Includes keyword optimization, formatting tips, and industry-specific customization.',
        'category': cat_chatgpt,
        'price': 24.99,
        'status': 'published',
        'tags': 'resume, job, career, ats',
        'views': 2345,
        'downloads': 678,
        'rating': 4.7,
        'rating_count': 189,
    },
]

print("\n📝 Creating prompts...")
created_count = 0
for data in prompts_data:
    prompt, created = Prompt.objects.get_or_create(
        title=data['title'],
        defaults={
            'author': admin,
            **{k: v for k, v in data.items() if k != 'title'}
        }
    )
    if created:
        created_count += 1
        print(f"✨ Created: {prompt.title} (${prompt.price})")
    else:
        print(f"✓ Exists: {prompt.title}")

print(f"\n✅ Database seeded successfully!")
print(f"📊 Summary:")
print(f"   - Categories: {Category.objects.count()}")
print(f"   - Prompts: {Prompt.objects.count()}")
print(f"   - New prompts: {created_count}")
print(f"   - Featured: {Prompt.objects.filter(featured=True).count()}")
print(f"   - Published: {Prompt.objects.filter(status='published').count()}")
