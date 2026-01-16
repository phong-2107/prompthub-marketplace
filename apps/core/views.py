"""
Core app views.
"""
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.db.models import Count, Q
from .models import Prompt, Category


def home(request):
    """
    Home page view - Digital Marketplace.
    Renders the main marketplace homepage with database data.
    """
    # Query featured prompts (hiển thị trên banner/popular section)
    featured_prompts = Prompt.objects.filter(
        status='published',
        featured=True
    ).select_related('category', 'author').order_by('-created_at')[:8]
    
    # Query trending prompts
    trending_prompts = Prompt.objects.filter(
        status='published',
        is_trending=True
    ).select_related('category', 'author').order_by('-views')[:6]
    
    # Query categories với số lượng products
    categories = Category.objects.annotate(
        product_count=Count('prompts', filter=Q(prompts__status='published'))
    ).order_by('-product_count')[:8]
    
    # Query new arrivals
    new_arrivals = Prompt.objects.filter(
        status='published'
    ).select_related('category', 'author').order_by('-created_at')[:12]
    
    # Best sellers (theo downloads)
    best_sellers = Prompt.objects.filter(
        status='published'
    ).select_related('category', 'author').order_by('-downloads')[:6]
    
    # Stats
    from django.db.models import Sum
    total_products = Prompt.objects.filter(status='published').count()
    total_downloads = Prompt.objects.aggregate(Sum('downloads'))['downloads__sum'] or 0
    total_categories = Category.objects.count()
    
    context = {
        'title': 'Home - PromptHub Digital Marketplace',
        'page': 'home',
        # Data từ database
        'featured_prompts': featured_prompts,
        'trending_prompts': trending_prompts,
        'categories': categories,
        'new_arrivals': new_arrivals,
        'best_sellers': best_sellers,
        # Stats
        'total_products': total_products,
        'total_downloads': total_downloads,
        'total_categories': total_categories,
    }
    return render(request, 'marketplace/home.html', context)


def about(request):
    """About page view."""
    context = {
        'title': 'About Us - PromptHub',
        'page': 'about',
    }
    return render(request, 'core/about.html', context)


class HomeView(TemplateView):
    """
    Class-based view for home page.
    Alternative implementation using CBV.
    """
    template_name = 'marketplace/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - PromptHub Digital Marketplace'
        context['page'] = 'home'
        return context
