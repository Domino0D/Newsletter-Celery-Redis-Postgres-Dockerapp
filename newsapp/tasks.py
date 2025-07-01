from celery import shared_task
from time import sleep

from django.utils import timezone
from datetime import timedelta

from django.core.mail import send_mail, EmailMessage
from .forms import SendMailToMe

from .models import UserSubmission
from django.contrib import messages

from django.shortcuts import redirect, render

from django.conf import settings
from .models import Newsletter, Subscriber 

from .forms import NewsletterForm


@shared_task
def send_feedback_email(email, message): # przykładowa funkcja
    sleep(5)
    send_mail(
        "Your feedback",
        f"\t{message}\n\nThank you",
        "eueuplpl@gmail.com",
        [email],
        fail_silently=False,
    )
    
@shared_task
def send_newsletter_email(newsletter_id, user_email):
    from .models import Newsletter, Subscriber  # import w funkcji, aby uniknąć problemów z cyklicznymi importami
    newsletter = Newsletter.objects.get(pk=newsletter_id)
    sleep(5)
    send_mail(
        subject=newsletter.subject,
        message=newsletter.content,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
    )  
    
    
@shared_task
def newsletter_sending_global(subject, content):
    emails = list(
        Subscriber.objects.filter(is_confirmed=True, Active_sub=True)
        .values_list('email', flat=True)
    )
    send_email = EmailMessage(
        subject,
        content,
        settings.EMAIL_HOST_USER,
        bcc=emails,
    )
    send_email.send()
    
@shared_task
def activate_link_email(confirmation_link, email):
    sleep(20)
    
    send_mail(
        'Potwierdź subskrypcję', #subject
        f'kliknij link, aby potwierdzić: {confirmation_link}', #content with confirm link
        settings.EMAIL_HOST_USER,
        [email], # new subscriber email
        fail_silently=False
    )
    
@shared_task
def activate_link_account(confirmation_link, email):
    sleep(20)
    
    send_mail(
            'Potwierdź swój adres email', #subject
            f'Kliknij w link, aby potwierdzić rejestrację: {confirmation_link}', #content with link
            settings.DEFAULT_FROM_EMAIL, #email settings from settings.py
            [email], #registering user email
            fail_silently=False, 
        )

