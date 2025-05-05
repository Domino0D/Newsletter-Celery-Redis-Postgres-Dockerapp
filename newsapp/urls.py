from django.urls import path
from .views import RegisterPage, CustomLoginView, CustomLogoutView, NewsletterCreate, NewsLetterUpdate, NewsLetterDelete, ConfirmEmailView, NewsletterDetailView, SubscribeView
from . import views


urlpatterns = [
    # path('home/', HomeView.as_view(),name='HomeView'),
    path('register/', RegisterPage.as_view(),name='RegisterPage'),
    path('login/', CustomLoginView.as_view(),name='CustomLoginView'),
    path('logout/', CustomLogoutView.as_view(),name='CustomLogoutView'),
    path('subcription_sent/', views.subscription_sent, name='subscription_sent'),
    path('adminpanel/', NewsletterCreate.as_view(),name='NewsletterCreate'),
    
    path('Newsletter/<int:pk>/', NewsletterDetailView.as_view(), name='newsletter-detail'),
    
    
    
    
    path('NewsLetterUpdate/<int:pk>/', NewsLetterUpdate.as_view(), name='NewsLetterUpdate'),    
    path('NewsLetterDelete/<int:pk>/', NewsLetterDelete.as_view(), name="NewsLetterDelete"),
    # path('SendSelfMessageView/<int:pk>/', SendSelfMessageView.as_view(), name='SendSelfMessageView'),    
    
    
    path('confirm-email/<uuid:token>/', ConfirmEmailView.as_view(), name='confirm_email'),

    
    path('', SubscribeView.as_view(), name='subscribe'),
    path('confirm/<uuid:token>/', views.confirm,name='Confirmation'),
]