from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import ToyDrawing


@receiver(post_save, sender=ToyDrawing)
def send_approval_email(sender, instance, created, **kwargs):
    if not created and instance.is_aproved:
        send_mail(
            subject='Your uploaded drawing has been approved',
            message=f'Dear {instance.user.username}, \nYour "{instance.name}" has been approved, Thank you for your time',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.user.email]
        )
