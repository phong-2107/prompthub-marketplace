"""
Django models for PromptHub database.
Chuyển đổi từ PostgreSQL schema sang Django ORM.
"""
from django.db import models
from django.contrib.auth import get_user_model
from apps.users.models import User

# =============================================
# PHẦN 1: AVATAR & BASIC MODELS
# =============================================

class Avatar(models.Model):
    """Avatar cho người dùng"""
    id_avatar = models.CharField(max_length=5, primary_key=True, db_column='id_avatar')
    avatar_url = models.URLField(max_length=255, blank=True, null=True, db_column='avatar_url')
    avatar_name = models.CharField(max_length=50, blank=True, null=True, db_column='avatar_name')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    
    class Meta:
        db_table = 'avatar'
        verbose_name = 'Avatar'
        verbose_name_plural = 'Avatars'
    
    def __str__(self):
        return self.avatar_name or self.id_avatar


# =============================================
# PHẦN 2: RBAC MODELS
# =============================================

class Role(models.Model):
    """Vai trò người dùng"""
    id_role = models.AutoField(primary_key=True, db_column='id_role')
    role_name = models.CharField(max_length=50, db_column='role_name')
    role_code = models.CharField(max_length=30, unique=True, db_column='role_code')
    description = models.CharField(max_length=255, blank=True, null=True)
    role_level = models.SmallIntegerField(default=1, db_column='role_level')
    active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
    
    def __str__(self):
        return self.role_name


class Permission(models.Model):
    """Quyền hạn"""
    id_permission = models.AutoField(primary_key=True, db_column='id_permission')
    parent_permission = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        db_column='parent_permission_id'
    )
    permission_name = models.CharField(max_length=50, db_column='permission_name')
    permission_code = models.CharField(max_length=50, unique=True, db_column='permission_code')
    module = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'permissions'
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'
    
    def __str__(self):
        return self.permission_name


class RolePermission(models.Model):
    """Gán quyền cho vai trò"""
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='id_role')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, db_column='id_permission')
    can_create = models.BooleanField(default=False, db_column='can_create')
    can_read = models.BooleanField(default=True, db_column='can_read')
    can_update = models.BooleanField(default=False, db_column='can_update')
    can_delete = models.BooleanField(default=False, db_column='can_delete')
    active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'role_permissions'
        unique_together = [['role', 'permission']]
        verbose_name = 'Role Permission'
        verbose_name_plural = 'Role Permissions'


# =============================================
# PHẦN 3: AI PLATFORMS & MODELS
# =============================================

class AIPlatform(models.Model):
    """Nền tảng AI (ChatGPT, Claude, Gemini...)"""
    id_platform = models.CharField(max_length=5, primary_key=True, db_column='id_platform')
    platform_name = models.CharField(max_length=50, db_column='platform_name')
    platform_code = models.CharField(max_length=30, unique=True, db_column='platform_code')
    company_name = models.CharField(max_length=100, blank=True, null=True, db_column='company_name')
    website = models.URLField(max_length=255, blank=True, null=True)
    logo_url = models.URLField(max_length=255, blank=True, null=True, db_column='logo_url')
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True, db_column='release_date')
    is_active = models.BooleanField(default=True, db_column='is_active')
    sort_order = models.IntegerField(default=0, db_column='sort_order')
    
    class Meta:
        db_table = 'ai_platforms'
        verbose_name = 'AI Platform'
        verbose_name_plural = 'AI Platforms'
        ordering = ['sort_order', 'platform_name']
    
    def __str__(self):
        return self.platform_name


class AIModel(models.Model):
    """Model AI cụ thể (GPT-4, Claude 3.5...)"""
    id_model = models.CharField(max_length=6, primary_key=True, db_column='id_model')
    platform = models.ForeignKey(AIPlatform, on_delete=models.CASCADE, db_column='id_platform')
    model_name = models.CharField(max_length=50, db_column='model_name')
    model_code = models.CharField(max_length=50, db_column='model_code')
    model_version = models.CharField(max_length=20, blank=True, null=True, db_column='model_version')
    description = models.TextField(blank=True, null=True)
    capabilities = models.JSONField(blank=True, null=True)  # ["text", "image", "code"]
    release_date = models.DateField(blank=True, null=True, db_column='release_date')
    is_latest = models.BooleanField(default=False, db_column='is_latest')
    is_active = models.BooleanField(default=True, db_column='is_active')
    
    class Meta:
        db_table = 'ai_models'
        verbose_name = 'AI Model'
        verbose_name_plural = 'AI Models'
    
    def __str__(self):
        return f"{self.platform.platform_name} - {self.model_name}"


# =============================================
# PHẦN 4: CATEGORIES & TAGS
# =============================================

class Category(models.Model):
    """Danh mục prompt"""
    id_category = models.CharField(max_length=5, primary_key=True, db_column='id_category')
    parent_category = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        db_column='parent_category_id'
    )
    category_name = models.CharField(max_length=50, db_column='category_name')
    category_code = models.CharField(max_length=30, unique=True, db_column='category_code')
    description = models.CharField(max_length=255, blank=True, null=True)
    icon_url = models.URLField(max_length=255, blank=True, null=True, db_column='icon_url')
    color_hex = models.CharField(max_length=7, blank=True, null=True, db_column='color_hex')
    sort_order = models.IntegerField(default=0, db_column='sort_order')
    active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['sort_order', 'category_name']
    
    def __str__(self):
        return self.category_name


class Tag(models.Model):
    """Tag cho prompt"""
    id_tag = models.AutoField(primary_key=True, db_column='id_tag')
    tag_name = models.CharField(max_length=30, db_column='tag_name')
    tag_slug = models.SlugField(max_length=50, unique=True, db_column='tag_slug')
    usage_count = models.IntegerField(default=0, db_column='usage_count')
    active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'tags'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
    
    def __str__(self):
        return self.tag_name


# =============================================
# PHẦN 5: PROMPT MODELS
# =============================================

class PromptSource(models.Model):
    """Nguồn prompt"""
    id_source = models.CharField(max_length=5, primary_key=True, db_column='id_source')
    source_name = models.CharField(max_length=100, db_column='source_name')
    source_url = models.URLField(max_length=255, blank=True, null=True, db_column='source_url')
    source_type = models.SmallIntegerField(default=1, db_column='source_type')
    description = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False, db_column='is_verified')
    active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'prompt_sources'
        verbose_name = 'Prompt Source'
        verbose_name_plural = 'Prompt Sources'
    
    def __str__(self):
        return self.source_name


class PromptAuthor(models.Model):
    """Tác giả prompt"""
    id_author = models.CharField(max_length=6, primary_key=True, db_column='id_author')
    author_name = models.CharField(max_length=100, db_column='author_name')
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        db_column='id_user'
    )
    email = models.EmailField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    social_links = models.JSONField(blank=True, null=True, db_column='social_links')
    bio = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False, db_column='is_verified')
    active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'prompt_authors'
        verbose_name = 'Prompt Author'
        verbose_name_plural = 'Prompt Authors'
    
    def __str__(self):
        return self.author_name


class PromptLevel(models.Model):
    """Cấp độ prompt"""
    id_level = models.SmallIntegerField(primary_key=True, db_column='id_level')
    level_name = models.CharField(max_length=30, db_column='level_name')
    level_code = models.CharField(max_length=20, db_column='level_code')
    description = models.CharField(max_length=100, blank=True, null=True)
    requires_premium = models.BooleanField(default=False, db_column='requires_premium')
    ticket_cost = models.SmallIntegerField(default=0, db_column='ticket_cost')
    active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'prompt_levels'
        verbose_name = 'Prompt Level'
        verbose_name_plural = 'Prompt Levels'
    
    def __str__(self):
        return self.level_name


class Prompt(models.Model):
    """Prompt chính"""
    
    STATUS_CHOICES = (
        (1, 'Draft'),
        (2, 'Pending'),
        (3, 'Published'),
        (4, 'Archived'),
    )
    
    id_prompt = models.CharField(max_length=12, primary_key=True, db_column='id_prompt')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    short_description = models.TextField(blank=True, null=True, db_column='short_description')
    
    author = models.ForeignKey(
        PromptAuthor, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        db_column='id_author'
    )
    source = models.ForeignKey(
        PromptSource, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        db_column='id_source'
    )
    level = models.ForeignKey(
        PromptLevel, 
        on_delete=models.SET_NULL, 
        null=True,
        db_column='id_level'
    )
    primary_category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        db_column='id_primary_category',
        related_name='primary_prompts'
    )
    
    thumbnail_url = models.URLField(max_length=255, blank=True, null=True, db_column='thumbnail_url')
    is_premium = models.BooleanField(default=False, db_column='is_premium')
    ticket_cost = models.SmallIntegerField(default=0, db_column='ticket_cost')
    is_featured = models.BooleanField(default=False, db_column='is_featured')
    is_verified = models.BooleanField(default=False, db_column='is_verified')
    
    # Statistics
    view_count = models.IntegerField(default=0, db_column='view_count')
    like_count = models.IntegerField(default=0, db_column='like_count')
    save_count = models.IntegerField(default=0, db_column='save_count')
    share_count = models.IntegerField(default=0, db_column='share_count')
    comment_count = models.IntegerField(default=0, db_column='comment_count')
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0,
        db_column='average_rating'
    )
    rating_count = models.IntegerField(default=0, db_column='rating_count')
    
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)
    published_at = models.DateTimeField(blank=True, null=True, db_column='published_at')
    
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_prompts',
        db_column='created_by'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='updated_prompts',
        db_column='updated_by'
    )
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')
    active = models.BooleanField(default=True)
    
    # Many-to-many relationships
    categories = models.ManyToManyField(Category, through='PromptCategory', related_name='prompts')
    tags = models.ManyToManyField(Tag, through='PromptTag', related_name='prompts')
    ai_models = models.ManyToManyField(AIModel, through='PromptAIModel', related_name='prompts')
    
    class Meta:
        db_table = 'prompts'
        verbose_name = 'Prompt'
        verbose_name_plural = 'Prompts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['created_by']),
        ]
    
    def __str__(self):
        return self.title


class PromptContent(models.Model):
    """Nội dung chi tiết prompt"""
    prompt = models.OneToOneField(
        Prompt, 
        on_delete=models.CASCADE, 
        primary_key=True,
        db_column='id_prompt',
        related_name='content'
    )
    prompt_text = models.TextField(db_column='prompt_text')
    prompt_text_en = models.TextField(blank=True, null=True, db_column='prompt_text_en')
    usage_guide = models.TextField(blank=True, null=True, db_column='usage_guide')
    example_input = models.TextField(blank=True, null=True, db_column='example_input')
    example_output = models.TextField(blank=True, null=True, db_column='example_output')
    tips = models.TextField(blank=True, null=True)
    variables = models.JSONField(blank=True, null=True)  # [{"name": "topic", "description": "..."}]
    
    class Meta:
        db_table = 'prompt_content'
        verbose_name = 'Prompt Content'
        verbose_name_plural = 'Prompt Contents'
    
    def __str__(self):
        return f"Content for {self.prompt.title}"


# Many-to-Many Through Models
class PromptCategory(models.Model):
    """Liên kết Prompt - Category"""
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, db_column='id_prompt')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='id_category')
    is_primary = models.BooleanField(default=False, db_column='is_primary')
    active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'prompt_categories'
        unique_together = [['prompt', 'category']]


class PromptTag(models.Model):
    """Liên kết Prompt - Tag"""
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, db_column='id_prompt')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, db_column='id_tag')
    
    class Meta:
        db_table = 'prompt_tags'
        unique_together = [['prompt', 'tag']]


class PromptAIModel(models.Model):
    """Liên kết Prompt - AI Model"""
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, db_column='id_prompt')
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE, db_column='id_model')
    is_recommended = models.BooleanField(default=False, db_column='is_recommended')
    compatibility_score = models.SmallIntegerField(
        blank=True, 
        null=True,
        db_column='compatibility_score'
    )
    notes = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'prompt_ai_models'
        unique_together = [['prompt', 'ai_model']]


# =============================================
# PHẦN 6: USER INTERACTIONS
# =============================================

class UserPromptInteraction(models.Model):
    """Tương tác người dùng với prompt"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_user')
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, db_column='id_prompt')
    is_liked = models.BooleanField(default=False, db_column='is_liked')
    is_saved = models.BooleanField(default=False, db_column='is_saved')
    rating = models.SmallIntegerField(blank=True, null=True)
    view_count = models.IntegerField(default=0, db_column='view_count')
    last_viewed_at = models.DateTimeField(blank=True, null=True, db_column='last_viewed_at')
    liked_at = models.DateTimeField(blank=True, null=True, db_column='liked_at')
    saved_at = models.DateTimeField(blank=True, null=True, db_column='saved_at')
    rated_at = models.DateTimeField(blank=True, null=True, db_column='rated_at')
    
    class Meta:
        db_table = 'user_prompt_interactions'
        unique_together = [['user', 'prompt']]
        verbose_name = 'User Prompt Interaction'
        verbose_name_plural = 'User Prompt Interactions'


class Comment(models.Model):
    """Bình luận"""
    
    STATUS_CHOICES = (
        (1, 'Visible'),
        (2, 'Hidden'),
        (3, 'Deleted'),
    )
    
    id_comment = models.AutoField(primary_key=True, db_column='id_comment')
    prompt = models.ForeignKey(
        Prompt, 
        on_delete=models.CASCADE, 
        related_name='comments',
        db_column='id_prompt'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_user')
    parent_comment = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='replies',
        db_column='parent_comment_id'
    )
    comment_text = models.TextField(db_column='comment_text')
    like_count = models.IntegerField(default=0, db_column='like_count')
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')
    
    class Meta:
        db_table = 'comments'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.prompt.title}"


# =============================================
# PHẦN 7: SUBSCRIPTION & PAYMENT
# =============================================

class SubscriptionPlan(models.Model):
    """Gói dịch vụ"""
    
    PLAN_TYPE_CHOICES = (
        (1, 'Free'),
        (2, 'Basic'),
        (3, 'Pro'),
        (4, 'Enterprise'),
    )
    
    id_plan = models.CharField(max_length=4, primary_key=True, db_column='id_plan')
    plan_name = models.CharField(max_length=50, db_column='plan_name')
    plan_code = models.CharField(max_length=20, unique=True, db_column='plan_code')
    plan_type = models.SmallIntegerField(choices=PLAN_TYPE_CHOICES, db_column='plan_type')
    duration_days = models.IntegerField(db_column='duration_days')
    ticket_amount = models.IntegerField(default=0, db_column='ticket_amount')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        db_column='discount_percent'
    )
    features = models.JSONField(blank=True, null=True)
    max_prompts_per_day = models.IntegerField(blank=True, null=True, db_column='max_prompts_per_day')
    can_access_premium = models.BooleanField(default=False, db_column='can_access_premium')
    can_download = models.BooleanField(default=False, db_column='can_download')
    can_use_api = models.BooleanField(default=False, db_column='can_use_api')
    sort_order = models.IntegerField(default=0, db_column='sort_order')
    is_popular = models.BooleanField(default=False, db_column='is_popular')
    active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'subscription_plans'
        verbose_name = 'Subscription Plan'
        verbose_name_plural = 'Subscription Plans'
        ordering = ['sort_order', 'plan_type']
    
    def __str__(self):
        return self.plan_name


# =============================================
# PHẦN 8: SYSTEM CONFIG
# =============================================

class SystemConfig(models.Model):
    """Cấu hình hệ thống"""
    config_key = models.CharField(max_length=50, primary_key=True, db_column='config_key')
    config_value = models.TextField(blank=True, null=True, db_column='config_value')
    config_type = models.CharField(max_length=20, default='string', db_column='config_type')
    description = models.CharField(max_length=255, blank=True, null=True)
    is_public = models.BooleanField(default=False, db_column='is_public')
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        db_column='updated_by'
    )
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')
    
    class Meta:
        db_table = 'system_config'
        verbose_name = 'System Config'
        verbose_name_plural = 'System Configs'
    
    def __str__(self):
        return self.config_key
