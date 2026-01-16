"""
Django Admin configuration for PromptHub models.
"""
from django.contrib import admin
from .models import (
    Avatar, Role, Permission, RolePermission,
    AIPlatform, AIModel, Category, Tag,
    PromptSource, PromptAuthor, PromptLevel, Prompt, PromptContent,
    PromptCategory, PromptTag, PromptAIModel,
    UserPromptInteraction, Comment, SubscriptionPlan, SystemConfig
)


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ['id_avatar', 'avatar_name', 'active']
    search_fields = ['avatar_name']
    list_filter = ['active']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['role_name', 'role_code', 'role_level', 'active']
    search_fields = ['role_name', 'role_code']
    list_filter = ['active', 'role_level']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['permission_name', 'permission_code', 'module', 'active']
    search_fields = ['permission_name', 'permission_code']
    list_filter = ['module', 'active']


@admin.register(AIPlatform)
class AIPlatformAdmin(admin.ModelAdmin):
    list_display = ['id_platform', 'platform_name', 'company_name', 'is_active', 'sort_order']
    search_fields = ['platform_name', 'company_name']
    list_filter = ['is_active']
    ordering = ['sort_order']


@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ['id_model', 'model_name', 'platform', 'is_latest', 'is_active']
    search_fields = ['model_name', 'model_code']
    list_filter = ['platform', 'is_latest', 'is_active']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id_category', 'category_name', 'parent_category', 'active', 'sort_order']
    search_fields = ['category_name', 'category_code']
    list_filter = ['active']
    ordering = ['sort_order']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['tag_name', 'tag_slug', 'usage_count', 'active']
    search_fields = ['tag_name', 'tag_slug']
    list_filter = ['active']
    prepopulated_fields = {'tag_slug': ('tag_name',)}


@admin.register(PromptSource)
class PromptSourceAdmin(admin.ModelAdmin):
    list_display = ['id_source', 'source_name', 'source_type', 'is_verified', 'active']
    search_fields = ['source_name']
    list_filter = ['source_type', 'is_verified', 'active']


@admin.register(PromptAuthor)
class PromptAuthorAdmin(admin.ModelAdmin):
    list_display = ['id_author', 'author_name', 'user', 'is_verified', 'active']
    search_fields = ['author_name', 'email']
    list_filter = ['is_verified', 'active']


@admin.register(PromptLevel)
class PromptLevelAdmin(admin.ModelAdmin):
    list_display = ['level_name', 'level_code', 'requires_premium', 'ticket_cost', 'active']
    search_fields = ['level_name', 'level_code']
    list_filter = ['requires_premium', 'active']


class PromptContentInline(admin.StackedInline):
    model = PromptContent
    extra = 0


class PromptCategoryInline(admin.TabularInline):
    model = PromptCategory
    extra = 1


class PromptTagInline(admin.TabularInline):
    model = PromptTag
    extra = 1


class PromptAIModelInline(admin.TabularInline):
    model = PromptAIModel
    extra = 1


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'slug', 'status', 'level', 'is_premium', 
        'view_count', 'like_count', 'created_by', 'created_at'
    ]
    search_fields = ['title', 'slug', 'short_description']
    list_filter = [
        'status', 'is_premium', 'is_featured', 'is_verified',
        'level', 'primary_category', 'created_at'
    ]
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = [
        'view_count', 'like_count', 'save_count', 'share_count',
        'comment_count', 'average_rating', 'rating_count',
        'created_at', 'updated_at'
    ]
    inlines = [PromptContentInline, PromptCategoryInline, PromptTagInline, PromptAIModelInline]
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('title', 'slug', 'short_description', 'thumbnail_url')
        }),
        ('Phân loại', {
            'fields': ('author', 'source', 'level', 'primary_category')
        }),
        ('Cài đặt', {
            'fields': ('is_premium', 'ticket_cost', 'is_featured', 'is_verified', 'status')
        }),
        ('Thống kê', {
            'fields': (
                'view_count', 'like_count', 'save_count', 'share_count',
                'comment_count', 'average_rating', 'rating_count'
            ),
            'classes': ('collapse',)
        }),
        ('Meta', {
            'fields': ('created_by', 'created_at', 'updated_by', 'updated_at', 'active')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id_comment', 'prompt', 'user', 'status', 'like_count', 'created_at']
    search_fields = ['comment_text', 'user__username', 'prompt__title']
    list_filter = ['status', 'created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = [
        'plan_name', 'plan_type', 'price', 'duration_days',
        'ticket_amount', 'is_popular', 'active'
    ]
    search_fields = ['plan_name', 'plan_code']
    list_filter = ['plan_type', 'is_popular', 'active']
    ordering = ['sort_order']


@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    list_display = ['config_key', 'config_type', 'is_public', 'updated_at']
    search_fields = ['config_key', 'description']
    list_filter = ['config_type', 'is_public']
    readonly_fields = ['updated_at']
