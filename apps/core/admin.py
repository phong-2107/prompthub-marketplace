from django.contrib import admin
from .models import Category, Prompt, Review, Purchase


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'price', 'status', 'featured', 'views', 'created_at']
    list_filter = ['status', 'featured', 'is_trending', 'category', 'created_at']
    search_fields = ['title', 'description', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'downloads', 'rating', 'rating_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('title', 'slug', 'description', 'content', 'category', 'tags')
        }),
        ('Giá và trạng thái', {
            'fields': ('price', 'original_price', 'status', 'featured', 'is_trending')
        }),
        ('Hình ảnh', {
            'fields': ('thumbnail', 'preview_images')
        }),
        ('Tác giả', {
            'fields': ('author',)
        }),
        ('Thống kê', {
            'fields': ('views', 'downloads', 'rating', 'rating_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['prompt', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['prompt__title', 'user__username', 'comment']
    readonly_fields = ['created_at']


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'prompt', 'price_paid', 'transaction_id', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'prompt__title', 'transaction_id']
    readonly_fields = ['created_at']
