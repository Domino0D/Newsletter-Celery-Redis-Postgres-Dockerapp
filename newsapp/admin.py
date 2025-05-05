from django.contrib import admin
from .models import Newsletter, Subscriber, UserSubmission

# Register your models here.

admin.site.register(Subscriber)
admin.site.register(Newsletter)
admin.site.register(UserSubmission)
