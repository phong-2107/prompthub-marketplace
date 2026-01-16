"""
Celery tasks for API app.
"""
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import time


@shared_task
def send_welcome_email(user_id):
    """
    Send welcome email to new user.
    
    Args:
        user_id: ID of the user
    
    Returns:
        str: Status message
    """
    from apps.users.models import User
    
    try:
        user = User.objects.get(id=user_id)
        send_mail(
            subject='Chào mừng đến với Django Project!',
            message=f'Xin chào {user.get_full_name()},\n\nCảm ơn bạn đã đăng ký!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return f'Welcome email sent to {user.email}'
    except User.DoesNotExist:
        return f'User with id {user_id} not found'
    except Exception as e:
        return f'Error sending email: {str(e)}'


@shared_task
def cleanup_old_data():
    """
    Periodic task to cleanup old data.
    Run this task daily using Celery Beat.
    
    Returns:
        str: Status message
    """
    # Add your cleanup logic here
    return 'Old data cleaned up successfully'


@shared_task
def generate_report(report_type):
    """
    Generate report asynchronously.
    
    Args:
        report_type: Type of report to generate
    
    Returns:
        str: Path to generated report
    """
    # Simulate long-running task
    time.sleep(5)
    
    return f'Report {report_type} generated successfully'


@shared_task(bind=True, max_retries=3)
def retry_task_example(self, param):
    """
    Example of a task with retry logic.
    
    Args:
        param: Task parameter
    
    Returns:
        str: Result message
    """
    try:
        # Simulate task that might fail
        if param < 0:
            raise ValueError('Invalid parameter')
        return f'Task completed with param: {param}'
    except Exception as exc:
        # Retry after 60 seconds
        raise self.retry(exc=exc, countdown=60)
