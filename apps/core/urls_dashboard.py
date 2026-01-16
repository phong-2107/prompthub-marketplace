"""
Dashboard URLs configuration
"""
from django.urls import path
from apps.core import views_dashboard

app_name = 'dashboard'

urlpatterns = [
    # Dashboard Home
    path('', views_dashboard.dashboard_home, name='home'),
    
    # Products/Prompts
    path('prompts/', views_dashboard.prompts_list, name='prompts'),
    path('prompts/create/', views_dashboard.prompts_list, name='prompt-create'),  # Placeholder
    path('prompts/<int:pk>/edit/', views_dashboard.prompts_list, name='prompt-edit'),  # Placeholder
    path('prompts/<int:pk>/delete/', views_dashboard.prompts_list, name='prompt-delete'),  # Placeholder
    
    # Categories
    path('categories/', views_dashboard.categories_list, name='categories'),
    path('categories/create/', views_dashboard.category_create, name='category-create'),
    path('categories/<int:pk>/edit/', views_dashboard.category_edit, name='category-edit'),
    path('categories/<int:pk>/delete/', views_dashboard.category_delete, name='category-delete'),
    
    # Sales
    path('sales/', views_dashboard.sales_list, name='sales'),
    
    # Reviews
    path('reviews/', views_dashboard.reviews_list, name='reviews'),
    
    # Users
    path('users/', views_dashboard.users_list, name='users'),
    
    # Earnings
    path('earnings/', views_dashboard.earnings_view, name='earnings'),
    
    # Settings
    path('settings/', views_dashboard.settings_view, name='settings'),
    path('profile/', views_dashboard.settings_view, name='profile'),  # Placeholder
    
    # Search
    path('search/', views_dashboard.search, name='search'),
]
