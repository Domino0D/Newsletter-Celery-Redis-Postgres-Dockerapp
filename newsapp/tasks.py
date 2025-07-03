from celery import shared_task
from time import sleep

from django.utils import timezone
from datetime import timedelta

from django.core.mail import send_mail, EmailMessage
from .forms import SendMailToMe

from django.contrib import messages

from django.shortcuts import redirect, render

from django.conf import settings
from .models import Newsletter, Subscriber 


    
@shared_task
def send_newsletter_email(newsletter_id, user_email):
    from .models import Newsletter, Subscriber  # import here to avoid circular imports
    newsletter = Newsletter.objects.get(pk=newsletter_id)  # get newsletter by id
    sleep(5)  # simulate delay (optional, e.g. for testing async behavior)
    send_mail(
        subject=newsletter.subject,  # email subject from newsletter
        message=newsletter.content,  # email content from newsletter
        from_email=settings.EMAIL_HOST_USER,  # sender email from settings
        recipient_list=[user_email],  # recipient email list with single user
        fail_silently=False,  # raise error if sending fails
    )  
    
@shared_task
def newsletter_sending_global(subject, content):
    emails = list(
        Subscriber.objects.filter(is_confirmed=True, Active_sub=True)
        .values_list('email', flat=True)
    )  # get list of confirmed and active subscriber emails
    send_email = EmailMessage(
        subject,  # email subject
        content,  # email body content
        settings.EMAIL_HOST_USER,  # sender email
        bcc=emails,  # blind carbon copy to all subscribers
    )
    send_email.send()  # send the email to all subscribers
    
@shared_task
def activate_link_email(confirmation_link, email):
    sleep(5)  # simulate delay before sending confirmation email
    send_mail(
        'Potwierdź subskrypcję',  # email subject in Polish: "Confirm subscription"
        f'kliknij link, aby potwierdzić: {confirmation_link}',  # email body with confirmation link
        settings.EMAIL_HOST_USER,  # sender email from settings
        [email],  # recipient email (new subscriber)
        fail_silently=False  # raise error if sending fails
    )
    
@shared_task
def activate_link_account(confirmation_link, email):
    sleep(5)  # simulate delay before sending account confirmation email
    send_mail(
        'Potwierdź swój adres email',  # subject: "Confirm your email address"
        f'Kliknij w link, aby potwierdzić rejestrację: {confirmation_link}',  # email body with registration confirmation link
        settings.DEFAULT_FROM_EMAIL,  # sender email from settings.py
        [email],  # recipient email (registering user)
        fail_silently=False,  # raise error if sending fails
    )

@shared_task
def send_feedback_email(email, message):  # example task to send feedback email
    sleep(5)  # simulate delay to check if backend works independently from frontend
    send_mail(
        "Your feedback",  # email subject
        f"\t{message}\n\nThank you",  # email body with the feedback message and thanks
        "eueuplpl@gmail.com",  # sender email address
        [email],  # recipient list with one email
        fail_silently=False,  # raise exception if sending fails
    )