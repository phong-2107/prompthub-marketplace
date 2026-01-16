"""
Custom User model.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Add custom fields as needed.
    """
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=15, blank=True, verbose_name='Số điện thoại')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Ảnh đại diện')
    bio = models.TextField(blank=True, verbose_name='Giới thiệu')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Ngày sinh')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        verbose_name = 'Người dùng'
        verbose_name_plural = 'Người dùng'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.username
    
    @property
    def full_name(self):
        """Return full name of user."""
        return f"{self.first_name} {self.last_name}".strip() or self.username
