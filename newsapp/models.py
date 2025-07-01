# newsletter/models.py
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

class Subscriber(models.Model):
    email = models.EmailField(unique=True) # email field to database and helps it with start form
    is_confirmed = models.BooleanField(default=False)
    confirmation_token = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    Active_sub = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.email} ({'Confirmed' if self.is_confirmed else 'Pending'})"

class Newsletter(models.Model):
    subject = models.CharField(max_length=200) # The subject of the newsletter
    content = models.TextField() # The content of the newsletter
    sent = models.BooleanField(default=False)  # Indicates if the newsletter has been sent 
    created_date = models.DateField(auto_now_add=True)  # Date when the newsletter was created
    updated_date = models.DateField(auto_now=True)  # Date when the newsletter was last updated
    
    def __str__(self):
        return self.subject # Returns the subject as the string represantion of the model 
    
    
class UserSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    newsletter = models.ForeignKey('Newsletter', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        indexes = [models.Index(fields=['user', 'timestamp'])]


class CustomUserCreationForm(UserCreationForm): #custom registration form
    email = forms.EmailField(required=True, label='Email') # email is required
    
    class Meta: # form config
        model = User # Basic django user model
        fields = [ 'email', 'username', 'password1', 'password2' ] #fields required for registration
        
    # def save(self, commit=True): #we saved user but not commit in database cause next user step is click authenticate link in email
    #     user = super().save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #     return user
    
class EmailConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #one to one field relation to relate user with token and confirmation
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) #UUID token, not editable, uniqe
    created_at = models.DateTimeField(auto_now_add=True)# Date when confirmation link was created
    is_confirmed = models.BooleanField(default=False) #by default, not confirmed
    
    profitability = models.FloatField(default=0.0)
    internet_page = models.URLField(blank=True, default='')
    
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(days=6)  # 1 day working