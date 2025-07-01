from django.shortcuts import render, get_object_or_404
from django.views import View

from time import sleep


from django.contrib.auth.views import LoginView

from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login, logout
from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from django.core.mail import send_mail, EmailMessage
from django.core import serializers


from .tasks import send_feedback_email, send_newsletter_email, newsletter_sending_global, activate_link_email, activate_link_account


from django.conf import settings
from .forms import SubscriptionForm, NewsletterForm, ActiveSubscriptionForm, SendMailToMe, FeedbackForm
from .models import Subscriber, Newsletter, CustomUserCreationForm, EmailConfirmation, UserSubmission
from django.http import Http404, HttpResponse

from django.utils import timezone
from datetime import timedelta

from django.contrib import messages


# Create your views here.

class CustomLogoutView(View): #standard logout view
    def get(self, request): #def get
        logout(request) #logout
        return redirect('/')  #redirect on home page

class RegisterPage(FormView): #Custom registration page
    template_name = 'register.html'
    form_class = CustomUserCreationForm # custom registration form
    redirect_authenticated_user = True
    success_url = reverse_lazy('HomeView')
    
    def form_valid(self, form): # if form is valid
        
        user = form.save(commit=False) # create user object, but not save to the database yet

        user.is_active = False # user is inactive until email confirmation
        user.save() # save the user to the database
        
        confirmation = EmailConfirmation.objects.create(user=user) # create an EmailConfirmation object linked to the user
        
        confirmation_link = self.request.build_absolute_uri( 
            reverse('confirm_email', args=[str(confirmation.token)])
        ) # build a unique confirmation link using the UUID token
        
        activate_link_account.delay(
            confirmation_link,
            user.email,
        )
        
        # activate_link_email.delay(
        #     confirmation_link,
        #     subscriber.email,
        # )
        # send_mail(
        #         'Potwierdź swój adres email', #subject
        #         f'Kliknij w link, aby potwierdzić rejestrację: {confirmation_link}', #content with link
        #         settings.DEFAULT_FROM_EMAIL, #email settings from settings.py
        #         [user.email], #registering user email
        #         fail_silently=False, 
        #     )
        return render(self.request, 'registration_pending.html') 
        
    def get(self, *args, **kwargs):
        
        if self.request.user.is_authenticated:
            return redirect('subscribe')
        else:
            return super().get(*args, **kwargs) #if user is log in and he try to go to register page we redirecting him on home page

class ConfirmEmailView(View):
    def get(self, request, token):
        confirmation = get_object_or_404(EmailConfirmation, token=token) # we get From emailconfirmation token, if it not exist return 404
        
        user = confirmation.user #user is = to confirmation user
        user.is_active = True #he is active now
        user.save() #save
        
        confirmation.is_confirmed = True #confirmation is confirmed in database
        confirmation.save() #save 
        
        login(request, user) #log the user in
        
        Subscriber.objects.update_or_create(email=user.email, defaults={'is_confirmed': True, 'user':user})# create or update a Subscriber object for this user/email
        
        if confirmation.is_confirmed: 
            return render(request, 'confirm_email.html', {'message': 'Email został potwierdzony', 'go_home': True}) #if confirmation succeeded
        if confirmation.is_expired():
            return render(request, 'confirm_email.html', {'message': 'Link wygasł', 'go_home': False}) # if the confirmation link expired

class CustomLoginView(LoginView):
    template_name = "login.html"
    fields = ['username', 'email', 'password']
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('subscribe')
    
    
class SubscribeView(View):
    
    def get(self, request): # When we sent HTTP GET
        newsletters = Newsletter.objects.filter(sent=True) #geting all send before newsletter
        form = SubscriptionForm() # geting form for save us to newsletter
        active_form = ActiveSubscriptionForm() # form to managing our subscribtion active
        
        return render(request, 'subscribe.html', {'form': form, 'active_form': active_form, 'newsletters':newsletters}) #returning request, site, first form, second form and newsletters

    def post(self, request): #when we sent HTTP POST
        newsletters = Newsletter.objects.filter(sent=True) # as in get
        form = SubscriptionForm(request.POST) # subscription form BUT when request is POST
        active_form = ActiveSubscriptionForm() #
        if "sent_sub" in request.POST: # if subscribing to newsletter
            if form.is_valid(): # if form is valid
                email = form.cleaned_data.get('email') # getting cleander email data (for doing thinks later)
                
                if Subscriber.objects.filter(email=email).exists(): # if email existing in our database
                    form.add_error('email', 'Ten email jest już zapisany!') #error 
                    return render(request, 'subscribe.html', {'form': form, 'newsletters':newsletters, 'active_form': active_form}) #return as in get
                else:
                    subscriber = form.save(commit=False) # create subcriber object, but not save in database
                    subscriber.save() #save
                    confirmation_link = request.build_absolute_uri(reverse(confirm, args=[subscriber.confirmation_token])) #creating confirmation link subscriber =confirmation _token
                    
                    activate_link_email.delay(
                        confirmation_link,
                        subscriber.email,
                    )
                    
                    
                return redirect('subscription_sent') #return to info site 
            return render(request, 'subscribe.html', {'form':form, 'newsletters':newsletters, 'active_form': active_form})
        elif 'actdis_sub' in request.POST: # if changing active state 
            subscriber = get_object_or_404(Subscriber, user=request.user) # if we cant find subscriber - http404
            active_form = ActiveSubscriptionForm(request.POST, instance=subscriber) # initializing form from forms.py - method post and relate with subsciber
            if active_form.is_valid():
                active_form.save() # save form if is it valid
            else:
                raise Http404('Coś poszło nie tak podczas zapisywania formularza. Spróbuj ponownie.') # error in other situation
            return render(request, 'subscribe.html', {'form': form, 'active_form': active_form, 'newsletters':newsletters}) # render as in get
        else:
            raise Http404('Coś poszło nie tak podczas przetwarzania formularza. Spróbuj ponownie.') # when error was before
        

def confirm(request, token): #confirmation subscription
    try: # try to get info about subscriber, token
        subscriber = Subscriber.objects.get(confirmation_token=token)
        subscriber.is_confirmed = True # if all is ok we set is confirmed as true
        subscriber.save() # and save all
        return render(request, 'confirmation_success.html') # render succes html
    except Subscriber.DoesNotExist: # if somethin goes wrong
        return render(request, 'confirmation_error.html') # return error html.
   
    
def subscription_sent(request):
    return render(request, "subscription_sent.html")
    
    
class NewsletterCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView): # View for creating a new newsletter, only accessible to superusers
    template_name = 'admin.html' #template
    model = Newsletter # model 
    fields = ['subject', 'content'] # Fields to be filled out in the form
    success_url = reverse_lazy('NewsletterCreate') # Redirect after succesful creation 
    
    def test_func(self):
        return self.request.user.is_superuser # Allow acces only to superuser
    
    def handle_no_permission(self):
        raise Http404('Site not found') # Raise the 404 error if the user is not a superuser
    
    def form_valid(self, form): # Handless form submission for both saving and sending the newsletter
        if not self.request.user.is_superuser:
            raise Http404('Site not found') # Additional security check
        
        if "save_news" in self.request.POST: # If the save button was clicked, set the current user as the author and save the newsletter 
            form.instance.user = self.request.user 
            newsletter = form.save()            
        
        elif "sent_news" in self.request.POST: # If the send button was clicked, send the newsletter to all active and confirmed subscribers
            subscribers = Subscriber.objects.filter(is_confirmed=True, Active_sub = True) # 
            emails = [s.email for s in subscribers] 
            form.instance.sent = True # Mark the newsletter as sent
            newsletter = form.save() # save newsletter
            
            subject = newsletter.subject
            content = newsletter.content
            
            newsletter_sending_global.delay(subject, content)
            
            # Send the newsletter via email to all subscribers
            send_mail( 
                newsletter.subject, # subject
                newsletter.content, # content
                settings.EMAIL_HOST_USER, # Sender's email address
                emails, # list of recipient email addresses
                fail_silently=False,
            )
        else:
            raise Http404('Coś poszło nie tak podczas wysyłania lub zapisywania newslettera') # If neither button was clicked, raise a 404 error
        
        return super().form_valid(form)
    def get_context_data(self, **kwargs): # Add all newsletters to the context for display in the template.
        context = super().get_context_data(**kwargs) 
        context['Newsletters'] = Newsletter.objects.all() 
        return context 

class NewsLetterUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView): #     View for updating an existing newsletter. Only accessible to superusers (administrators).
    model = Newsletter # The model to update
    fields = ['subject', 'content'] # Fields that can be edited
    template_name = "newsletter_form.html" # Template for the update form
    success_url = reverse_lazy('NewsletterCreate') # Redirect after successful update
    
    def test_func(self):
        return self.request.user.is_superuser # Allow acces only for superusers
    
    def handle_no_permission(self):
        raise Http404('Site not found') # Raise a 404 error if the user is not superuser
    
    def form_valid(self, form): # Handles form submission for both saving and sending the updated newsletter.
        if "save_news" in self.request.POST: # If the save button was clicked, set the current user as the author and save the newsletter
            form.instance.user = self.request.user
            newsletter = form.save()

        elif "sent_news" in self.request.POST: # If sent button is clicked, sent newsletter to active and confirmed subscribers and save newsletter
            subscribers = Subscriber.objects.filter(is_confirmed=True, Active_sub=True) # active and confirmed subscribers
            emails = [s.email for s in subscribers] # email of subscribers
            form.instance.sent = True # Mark the newsletter as send
            newsletter = form.save() # save the newsletter
            
            # Send the newsletter via email to all subscribers 
            
            send_email = EmailMessage(
                newsletter.subject, # subject 
                newsletter.content, # content
                settings.EMAIL_HOST_USER, # Sender's email address 
                bcc=emails, # List of recipient 
            )
        else: # If neither button was clicked, raise a 404 error
            raise Http404('Coś poszło nie tak podczas wysyłania lub zapisywania newslettera')
        return super().form_valid(form)


class NewsLetterDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # standard django delete view
    template_name = 'newsletter_confirm_delete.html' 
    model = Newsletter
    context_object_name = 'newsletter'
    success_url = reverse_lazy('NewsletterCreate')
    
    def test_func(self):
        return self.request.user.is_superuser # Allow acces only to superuser
    
    def handle_no_permission(self):
        raise Http404('Site not found') # Raise the 404 error if the user is not a superuser
    
    
class NewsletterDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = Newsletter
    template_name = 'newsletter_detail.html'
    context_object_name = 'newsletter'

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        raise Http404('Musisz się zalogować aby widzieć tę stronę')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['send_form'] = SendMailToMe()
        return context

    def post(self, request, *args, **kwargs):
        newsletter = self.get_object()
        form = SendMailToMe(request.POST)
        one_day_ago = timezone.now() - timedelta(hours=24)

        recent_submission = UserSubmission.objects.filter(
            user=request.user,
            newsletter=newsletter,
            timestamp__gte=one_day_ago
        ).exists()

        if recent_submission:
            messages.error(request, "Możesz wysłać ten newsletter do siebie tylko raz na 24 godziny.")
            return redirect('newsletter-detail', pk=newsletter.pk)

        if form.is_valid():
            # Wywołanie zadania Celery asynchronicznie
            send_newsletter_email.delay(newsletter.pk, request.user.email)

            # Zapisujemy informację o wysłaniu
            UserSubmission.objects.create(user=request.user, newsletter=newsletter)

            messages.success(request, "Wiadomość została wysłana! Sprawdź folder spam.")
            return redirect('newsletter-detail', pk=newsletter.pk)
        else:
            return render(request, self.template_name, {'send_form': form, 'newsletter': newsletter})

class FeedbackFormView(FormView):
    template_name = "feedback.html"
    form_class = FeedbackForm
    success_url = '/feedback/'
    
    def form_valid(self, form):
        send_feedback_email.delay(
            email=form.cleaned_data['email'],
            message=form.cleaned_data['message']
        )
        
        return super().form_valid(form)
            

    
    
        

