from django.urls import path, include
from django_auth import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('home/', views.landing_page, name='home'),
]
