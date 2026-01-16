"""
Management command để setup database PromptHub.
Usage: python manage.py setup_prompthub_db
"""
from django.core.management.base import BaseCommand
from django.db import connection
import os


class Command(BaseCommand):
    help = 'Setup PromptHub database với schema và seed data'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--seed',
            action='store_true',
            help='Import seed data sau khi chạy migrations',
        )
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset database (xóa tất cả tables của PromptHub)',
        )
    
    def handle(self, *args, **options):
        """Handle the command."""
        if options['reset']:
            self.reset_database()
        
        self.stdout.write('Running migrations...')
        from django.core.management import call_command
        call_command('migrate', 'prompthub')
        
        if options['seed']:
            self.import_seed_data()
        
        self.stdout.write(self.style.SUCCESS('Database setup completed!'))
    
    def reset_database(self):
        """Reset PromptHub tables."""
        self.stdout.write(self.style.WARNING('Resetting PromptHub database...'))
        
        # Confirm
        confirm = input('This will delete all PromptHub data. Continue? (yes/no): ')
        if confirm.lower() != 'yes':
            self.stdout.write('Aborted.')
            return
        
        with connection.cursor() as cursor:
            # Get all tables from prompthub app
            cursor.execute("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public' 
                AND tablename LIKE 'prompt%' 
                OR tablename IN ('avatar', 'roles', 'permissions', 'ai_platforms', 'ai_models', 
                                'categories', 'tags', 'user_collections', 'subscription_plans',
                                'system_config', 'comments', 'notifications')
            """)
            tables = cursor.fetchall()
            
            # Drop tables
            for table in tables:
                cursor.execute(f'DROP TABLE IF EXISTS {table[0]} CASCADE')
        
        self.stdout.write(self.style.SUCCESS('Database reset completed!'))
    
    def import_seed_data(self):
        """Import seed data."""
        from apps.prompthub.models import (
            Role, Permission, PromptLevel, AIPlatform, AIModel,
            Category, SubscriptionPlan, SystemConfig
        )
        
        self.stdout.write('Importing seed data...')
        
        # Roles
        roles_data = [
            {'role_name': 'Khách', 'role_code': 'GUEST', 'description': 'Người dùng chưa đăng nhập', 'role_level': 1},
            {'role_name': 'Thành viên', 'role_code': 'MEMBER', 'description': 'Thành viên miễn phí', 'role_level': 2},
            {'role_name': 'Premium', 'role_code': 'PREMIUM', 'description': 'Thành viên trả phí', 'role_level': 3},
            {'role_name': 'Biên tập viên', 'role_code': 'EDITOR', 'description': 'Quản lý nội dung', 'role_level': 5},
            {'role_name': 'Moderator', 'role_code': 'MODERATOR', 'description': 'Kiểm duyệt nội dung', 'role_level': 6},
            {'role_name': 'Quản trị viên', 'role_code': 'ADMIN', 'description': 'Quản trị hệ thống', 'role_level': 10},
        ]
        for data in roles_data:
            Role.objects.get_or_create(role_code=data['role_code'], defaults=data)
        self.stdout.write('✓ Roles imported')
        
        # Permissions
        permissions_data = [
            {'permission_name': 'Xem prompt', 'permission_code': 'prompt.view', 'module': 'prompt'},
            {'permission_name': 'Tạo prompt', 'permission_code': 'prompt.create', 'module': 'prompt'},
            {'permission_name': 'Sửa prompt', 'permission_code': 'prompt.edit', 'module': 'prompt'},
            {'permission_name': 'Xóa prompt', 'permission_code': 'prompt.delete', 'module': 'prompt'},
            {'permission_name': 'Xem premium', 'permission_code': 'prompt.view_premium', 'module': 'prompt'},
        ]
        for data in permissions_data:
            Permission.objects.get_or_create(permission_code=data['permission_code'], defaults=data)
        self.stdout.write('✓ Permissions imported')
        
        # Prompt Levels
        levels_data = [
            {'id_level': 1, 'level_name': 'Cơ bản', 'level_code': 'BASIC', 'ticket_cost': 0},
            {'id_level': 2, 'level_name': 'Trung cấp', 'level_code': 'INTERMEDIATE', 'ticket_cost': 0},
            {'id_level': 3, 'level_name': 'Nâng cao', 'level_code': 'ADVANCED', 'ticket_cost': 1},
            {'id_level': 4, 'level_name': 'Chuyên gia', 'level_code': 'EXPERT', 'ticket_cost': 2, 'requires_premium': True},
            {'id_level': 5, 'level_name': 'Premium', 'level_code': 'PREMIUM', 'ticket_cost': 5, 'requires_premium': True},
        ]
        for data in levels_data:
            PromptLevel.objects.get_or_create(id_level=data['id_level'], defaults=data)
        self.stdout.write('✓ Prompt Levels imported')
        
        # AI Platforms
        platforms_data = [
            {'id_platform': 'AI001', 'platform_name': 'ChatGPT', 'platform_code': 'chatgpt', 'company_name': 'OpenAI'},
            {'id_platform': 'AI002', 'platform_name': 'Claude', 'platform_code': 'claude', 'company_name': 'Anthropic'},
            {'id_platform': 'AI003', 'platform_name': 'Gemini', 'platform_code': 'gemini', 'company_name': 'Google'},
            {'id_platform': 'AI004', 'platform_name': 'Copilot', 'platform_code': 'copilot', 'company_name': 'Microsoft'},
        ]
        for data in platforms_data:
            AIPlatform.objects.get_or_create(id_platform=data['id_platform'], defaults=data)
        self.stdout.write('✓ AI Platforms imported')
        
        # Categories
        categories_data = [
            {'id_category': 'CA001', 'category_name': 'Viết lách', 'category_code': 'writing'},
            {'id_category': 'CA002', 'category_name': 'Lập trình', 'category_code': 'coding'},
            {'id_category': 'CA003', 'category_name': 'Marketing', 'category_code': 'marketing'},
            {'id_category': 'CA004', 'category_name': 'Giáo dục', 'category_code': 'education'},
            {'id_category': 'CA005', 'category_name': 'Kinh doanh', 'category_code': 'business'},
        ]
        for data in categories_data:
            Category.objects.get_or_create(id_category=data['id_category'], defaults=data)
        self.stdout.write('✓ Categories imported')
        
        # Subscription Plans
        plans_data = [
            {
                'id_plan': 'PL01', 'plan_name': 'Miễn phí', 'plan_code': 'FREE',
                'plan_type': 1, 'duration_days': 36500, 'ticket_amount': 5,
                'price': 0, 'can_access_premium': False
            },
            {
                'id_plan': 'PL02', 'plan_name': 'Basic Tháng', 'plan_code': 'BASIC_MONTH',
                'plan_type': 2, 'duration_days': 30, 'ticket_amount': 50,
                'price': 49000, 'can_access_premium': False
            },
            {
                'id_plan': 'PL03', 'plan_name': 'Pro Tháng', 'plan_code': 'PRO_MONTH',
                'plan_type': 3, 'duration_days': 30, 'ticket_amount': 200,
                'price': 149000, 'can_access_premium': True
            },
        ]
        for data in plans_data:
            SubscriptionPlan.objects.get_or_create(id_plan=data['id_plan'], defaults=data)
        self.stdout.write('✓ Subscription Plans imported')
        
        self.stdout.write(self.style.SUCCESS('All seed data imported successfully!'))
