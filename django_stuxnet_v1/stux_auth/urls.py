from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name="signup"),
    path('verify/', views.verify, name="verify"),
    path('login/', views.logIn, name="login"),
    path('logout/', views.logOut, name="logout"),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('change_password/<pk>', views.change_password, name='change_password'),
]

"""
Add phone verification url:
path('verify-phone/', views.verify_phone, name="verify_phone")
"""