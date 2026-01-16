from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Category(models.Model):
    """Danh mục prompt"""
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Icon class")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Prompt(models.Model):
    """Sản phẩm Prompt"""
    
    STATUS_CHOICES = [
        ('draft', 'Nháp'),
        ('published', 'Đã xuất bản'),
        ('suspended', 'Đã tạm dừng'),
    ]
    
    # Thông tin cơ bản
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Mô tả ngắn")
    content = models.TextField(verbose_name="Nội dung chi tiết")
    
    # Phân loại
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT,
        related_name='prompts',
        verbose_name="Danh mục"
    )
    tags = models.CharField(max_length=255, blank=True, verbose_name="Tags (phân cách bằng dấu phẩy)")
    
    # Giá và trạng thái
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá")
    original_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Giá gốc (để hiển thị giảm giá)"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft',
        verbose_name="Trạng thái"
    )
    
    # Hình ảnh
    thumbnail = models.ImageField(
        upload_to='prompts/thumbnails/%Y/%m/', 
        verbose_name="Ảnh thumbnail"
    )
    preview_images = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Ảnh preview (list URLs)"
    )
    
    # Tác giả
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='prompts',
        verbose_name="Tác giả"
    )
    
    # Thống kê
    views = models.PositiveIntegerField(default=0, verbose_name="Lượt xem")
    downloads = models.PositiveIntegerField(default=0, verbose_name="Lượt tải")
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00,
        verbose_name="Đánh giá trung bình"
    )
    rating_count = models.PositiveIntegerField(default=0, verbose_name="Số đánh giá")
    
    # Flags
    featured = models.BooleanField(default=False, verbose_name="Nổi bật")
    is_trending = models.BooleanField(default=False, verbose_name="Đang thịnh hành")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Prompt"
        verbose_name_plural = "Prompts"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['featured', '-created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def discount_percentage(self):
        """Tính % giảm giá"""
        if self.original_price and self.original_price > self.price:
            return int((self.original_price - self.price) / self.original_price * 100)
        return 0
    
    @property
    def is_on_sale(self):
        """Kiểm tra có đang giảm giá không"""
        return self.discount_percentage > 0
    
    def get_tags_list(self):
        """Chuyển tags string thành list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []


class Review(models.Model):
    """Đánh giá sản phẩm"""
    prompt = models.ForeignKey(
        Prompt,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Prompt"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Người đánh giá"
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name="Số sao (1-5)"
    )
    comment = models.TextField(verbose_name="Bình luận")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Đánh giá"
        verbose_name_plural = "Đánh giá"
        ordering = ['-created_at']
        unique_together = ['prompt', 'user']  # Mỗi user chỉ review 1 lần
    
    def __str__(self):
        return f"{self.user.username} - {self.prompt.title} ({self.rating}★)"


class Purchase(models.Model):
    """Lịch sử mua hàng"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name="Người mua"
    )
    prompt = models.ForeignKey(
        Prompt,
        on_delete=models.PROTECT,
        related_name='purchases',
        verbose_name="Prompt"
    )
    price_paid = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Giá đã thanh toán"
    )
    transaction_id = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name="Mã giao dịch"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày mua")
    
    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.prompt.title}"
