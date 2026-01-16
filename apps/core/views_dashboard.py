"""
Dashboard views for admin interface
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta
from apps.core.models import Prompt, Category, Review, Purchase
from django.contrib.auth import get_user_model

User = get_user_model()


def is_staff_or_superuser(user):
    """Check if user is staff or superuser"""
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_staff_or_superuser)
def dashboard_home(request):
    """Dashboard home page with statistics"""
    
    # Calculate stats
    total_products = Prompt.objects.filter(status='published').count()
    total_sales = Purchase.objects.count()
    total_downloads = Prompt.objects.aggregate(Sum('downloads'))['downloads__sum'] or 0
    total_earnings = Purchase.objects.aggregate(Sum('price_paid'))['price_paid__sum'] or 0
    
    stats = {
        'total_products': total_products,
        'total_sales': total_sales,
        'total_downloads': total_downloads,
        'total_earnings': f'${total_earnings:.2f}',
    }
    
    # User balance (mock data - replace with real calculation)
    user_balance = 580.00
    
    # Top countries (mock data - replace with real data from Purchase model)
    top_countries = [
        {'name': 'United States', 'flag': 'assets/images/thumbs/flag1.png', 'amount': 58.00},
        {'name': 'Mexico', 'flag': 'assets/images/thumbs/flag2.png', 'amount': 69.00},
        {'name': 'Brazil', 'flag': 'assets/images/thumbs/flag3.png', 'amount': 120.00},
        {'name': 'Canada', 'flag': 'assets/images/thumbs/flag4.png', 'amount': 25.00},
        {'name': 'Ireland', 'flag': 'assets/images/thumbs/flag5.png', 'amount': 85.00},
    ]
    
    # Recent sales (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_sales = Purchase.objects.filter(
        created_at__gte=thirty_days_ago
    ).values('created_at__date').annotate(
        items_count=Count('id'),
        amount=Sum('price_paid')
    ).order_by('-created_at__date')[:13]
    
    # Sales data for chart (last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    sales_by_day = Purchase.objects.filter(
        created_at__gte=seven_days_ago
    ).values('created_at__date').annotate(
        total=Sum('price_paid')
    ).order_by('created_at__date')
    
    sales_labels = [sale['created_at__date'].strftime('%b %d') for sale in sales_by_day]
    sales_data = [float(sale['total']) for sale in sales_by_day]
    
    context = {
        'stats': stats,
        'user_balance': user_balance,
        'top_countries': top_countries,
        'recent_sales': recent_sales,
        'sales_labels': sales_labels,
        'sales_data': sales_data,
    }
    
    return render(request, 'dashboard/home.html', context)


@login_required
@user_passes_test(is_staff_or_superuser)
def prompts_list(request):
    """List all prompts with filters"""
    
    prompts = Prompt.objects.select_related('category', 'author').all()
    
    # Filters
    category_id = request.GET.get('category')
    status = request.GET.get('status')
    search = request.GET.get('q')
    
    if category_id:
        prompts = prompts.filter(category_id=category_id)
    
    if status:
        prompts = prompts.filter(status=status)
    
    if search:
        prompts = prompts.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(tags__icontains=search)
        )
    
    # Order by latest
    prompts = prompts.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(prompts, 20)
    page = request.GET.get('page', 1)
    prompts_page = paginator.get_page(page)
    
    # Get all categories for filter dropdown
    categories = Category.objects.all()
    
    context = {
        'prompts': prompts_page,
        'categories': categories,
    }
    
    return render(request, 'dashboard/prompts_list.html', context)


@login_required
@user_passes_test(is_staff_or_superuser)
def categories_list(request):
    """List all categories"""
    
    categories = Category.objects.annotate(
        product_count=Count('prompts', filter=Q(prompts__status='published'))
    ).order_by('-product_count')
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'dashboard/categories_list.html', context)


@login_required
@user_passes_test(is_staff_or_superuser)
def category_create(request):
    """Create new category"""
    
    if request.method == 'POST':
        name = request.POST.get('name')
        icon = request.POST.get('icon', '')
        description = request.POST.get('description', '')
        
        if name:
            Category.objects.create(
                name=name,
                icon=icon,
                description=description
            )
            messages.success(request, f'Category "{name}" created successfully!')
        else:
            messages.error(request, 'Category name is required!')
    
    return redirect('dashboard:categories')


@login_required
@user_passes_test(is_staff_or_superuser)
def category_edit(request, pk):
    """Edit category"""
    
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.icon = request.POST.get('icon', '')
        category.description = request.POST.get('description', '')
        category.save()
        
        messages.success(request, f'Category "{category.name}" updated successfully!')
    
    return redirect('dashboard:categories')


@login_required
@user_passes_test(is_staff_or_superuser)
def category_delete(request, pk):
    """Delete category"""
    
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f'Category "{name}" deleted successfully!')
    
    return redirect('dashboard:categories')


@login_required
@user_passes_test(is_staff_or_superuser)
def sales_list(request):
    """List all sales/purchases"""
    
    purchases = Purchase.objects.select_related(
        'user', 'prompt', 'prompt__category'
    ).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(purchases, 20)
    page = request.GET.get('page', 1)
    purchases_page = paginator.get_page(page)
    
    context = {
        'purchases': purchases_page,
    }
    
    return render(request, 'dashboard/sales_list.html', context)


@login_required
@user_passes_test(is_staff_or_superuser)
def reviews_list(request):
    """List all reviews"""
    
    reviews = Review.objects.select_related(
        'user', 'prompt'
    ).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(reviews, 20)
    page = request.GET.get('page', 1)
    reviews_page = paginator.get_page(page)
    
    context = {
        'reviews': reviews_page,
    }
    
    return render(request, 'dashboard/reviews_list.html', context)


@login_required
@user_passes_test(is_staff_or_superuser)
def users_list(request):
    """List all users"""
    
    users = User.objects.annotate(
        prompts_count=Count('prompts'),
        purchases_count=Count('purchases')
    ).order_by('-date_joined')
    
    # Pagination
    paginator = Paginator(users, 20)
    page = request.GET.get('page', 1)
    users_page = paginator.get_page(page)
    
    context = {
        'users': users_page,
    }
    
    return render(request, 'dashboard/users_list.html', context)


@login_required
@user_passes_test(is_staff_or_superuser)
def earnings_view(request):
    """Earnings overview"""
    
    # Total earnings
    total = Purchase.objects.aggregate(Sum('price_paid'))['price_paid__sum'] or 0
    
    # Earnings by month
    from django.db.models.functions import TruncMonth
    monthly_earnings = Purchase.objects.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        total=Sum('price_paid')
    ).order_by('-month')[:12]
    
    context = {
        'total_earnings': total,
        'monthly_earnings': monthly_earnings,
    }
    
    return render(request, 'dashboard/earnings.html', context)


@login_required
@user_passes_test(is_staff_or_superuser)
def settings_view(request):
    """Settings page"""
    
    context = {}
    
    return render(request, 'dashboard/settings.html', context)


@login_required
@user_passes_test(is_staff_or_superuser)
def search(request):
    """Search across dashboard"""
    
    query = request.GET.get('q', '')
    
    results = {
        'prompts': Prompt.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )[:10],
        'categories': Category.objects.filter(name__icontains=query)[:5],
        'users': User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )[:5],
    }
    
    context = {
        'query': query,
        'results': results,
    }
    
    return render(request, 'dashboard/search_results.html', context)
