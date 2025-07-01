# users/forms.py
from django import forms # importing django forms
from django.contrib.auth.forms import UserCreationForm  #UserCreation form method 
from .models import Subscriber, Newsletter #importing models
from django_recaptcha.fields import ReCaptchaField # type: ignore #importing google captcha

class SubscriptionForm(forms.ModelForm): # subscription form 
    captcha = ReCaptchaField() #adding google captcha

    class Meta: # creation form
        model = Subscriber # model 
        fields = ['email'] #required fields (email form)

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if Subscriber.objects.filter(email=email).exists():
    #         raise forms.ValidationError('Ten email jest już zapisany do newslette12ra.')
    #     return email
       
class ActiveSubscriptionForm(forms.ModelForm): # form to managing subscription active
    class Meta: # creating form 
        model = Subscriber # model
        fields = ['Active_sub'] # required fields (checkbox)
        
class NewsletterForm(forms.ModelForm): # standard django ModelForm 
    
    class Meta: 
        model = Newsletter # The model associated with this form 
        fields = ['subject', 'content'] # Fields to be included in the form 
        
class SendMailToMe(forms.Form):
    captcha = ReCaptchaField()
    

class FeedbackForm(forms.Form):
    email = forms.EmailField(label="Email Address")
    message = forms.CharField(
        label="Message", widget=forms.Textarea(attrs={"rows": 5})
    )