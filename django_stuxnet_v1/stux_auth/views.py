from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import CustomUser, OneTimePassword
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from allauth.socialaccount.models import SocialAccount
import datetime
import random
import math
import os
from twilio.rest import Client
import time
from django.urls import reverse
from django.contrib.auth.hashers import check_password

# Create your views here.

account_sid = "ACbddfd66a3e5ce24ee5992dfe7f790ef2"
auth_token = "c8e8ee90a80f15968024905e370dd86a"
null_phone = "xxxxxxxxxxxxxxx"

def send_code(code, number):
    account_sid = 'ACbddfd66a3e5ce24ee5992dfe7f790ef2' 
    auth_token = 'c8e8ee90a80f15968024905e370dd86a' 
    client = Client(account_sid, auth_token) 
    
    message = client.messages.create(  
                                messaging_service_sid='MGa2faf3770061ef9f4096704707c987ca', 
                                body=f"{code}",      
                                to=number 
                            ) 
    

    return message.sid


def OTP():
    otp = [str(math.floor(random.randrange(0, 10) * random.random())) for i in range(6)]
    otp = "".join(otp)
    return otp

def signup(request):
    context = {
        "error_messages": []
    }
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        password_valid = password1 == password2
        user_valid = False
        try:
            User.objects.get(email=email)
            user_valid = False
        except ObjectDoesNotExist:
            user_valid = True
        if user_valid == False:
            context['error_messages'].append('Email already exists')
        if password_valid == False:
            context['error_messages'].append('Passwords do not match')
        
        if user_valid and password_valid:
            user = User.objects.create_user(f'user {datetime.datetime.now()}', email, password1)
            user.username = f'user{user.id}'
            user.first_name = fname
            user.last_name = lname
            user.save()
            customuser = CustomUser.objects.create(user=user, phone=null_phone)
            customuser.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('verify')
        

    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'stux_auth/signup.html', context)


def verify(request):
    context = {
        'error_messages': [], 
        'infos': []
    }
    
                

    if (request.user.is_authenticated) and (CustomUser.objects.get(user=request.user).email_verified == False):
        email = request.user.email
        try:
            l = OneTimePassword.objects.get(user=request.user, type=0)
            then_sec = int(l.time)
            time=datetime.datetime.now()
            time_sec = ((int(time.year) * 31536000) + (int(time.month) * 2592000) + (int(time.day) * 86400) + (int(time.hour) * 3600) + (int(time.minute) * 60) + (int(time.second)))
            if time_sec - then_sec >= 1800:
                l.delete()
                o = OneTimePassword.objects.create(otp=OTP(), user=request.user, time=time_sec, type=0)
                o.save()
                send_mail(
                'This is your code.', 
                o.otp, 
                'unknown@gmail.com', 
                [email], 
                fail_silently=False)
                context['error_messages'].append('The code we sent has expired.')
                context['infos'].append('A new code has been sent to your email.')
        except ObjectDoesNotExist:
            time=datetime.datetime.now()
            time_sec = ((int(time.year) * 31536000) + (int(time.month) * 2592000) + (int(time.day) * 86400) + (int(time.hour) * 3600) + (int(time.minute) * 60) + (int(time.second)))
            on = OneTimePassword.objects.create(otp=OTP(), user=request.user, time=time_sec, type=0)
            on.save()
            send_mail(
                'This is your code.', 
                on.otp, 
                'unknown@gmail.com', 
                [email], 
                fail_silently=False)
            context['infos'].append('A code has been sent to your email.')
        if request.method == "POST":
            if 'resend' in request.POST:
                for l in list(OneTimePassword.objects.filter(user=request.user, type=0)):
                    l.delete()
                time=datetime.datetime.now()
                time_sec = str((int(time.year) * 31536000) + (int(time.month) * 2592000) + (int(time.day) * 86400) + (int(time.hour) * 3600) + (int(time.minute) * 60) + (int(time.second)))
                o = OneTimePassword.objects.create(otp=OTP(), user=request.user, time=time_sec, type=0)
                o.save()
                
                send_mail(
                    'This is your code.', 
                    o.otp, 
                    'davidukemeekong1@gmail.com', 
                    [request.user.email], 
                    fail_silently=False)
                context['infos'].append('A code has been sent to your email.')

            else:
                code = request.POST['code']
                l = OneTimePassword.objects.get(user=request.user, type=0)
                now = datetime.datetime.now()
                then_sec = int(l.time)
                sec = (int(now.year) * 31536000) + (int(now.month) * 2592000) + (int(now.day) * 86400) + (int(now.hour) * 3600) + (int(now.minute) * 60) + (int(now.second))
                if sec - then_sec < 1800:
                    if code == l.otp:
                        l.delete()
                        c = CustomUser.objects.get(user=request.user)
                        c.email_verified = True
                        c.save()
                        return redirect('home')
                    else:
                        context['error_messages'].append('Code is invalid.')
                else:
                    l.delete()
                    context['error_messages'].append('The code has expired.')
                    on = OneTimePassword.objects.create(otp=OTP(), user=request.user, time=datetime.datetime.now(), type=0)
                    on.save()
                    send_mail(
                    'This is your code.', 
                    on.otp, 
                    'unknown@gmail.com', 
                    [request.user.email], 
                    fail_silently=False)
                    context['infos'].append('A new code has been sent to your email.')

        return render(request, 'stux_auth/verification.html', context=context)
    else:
        return HttpResponse("<h1>You don't have access to this page</h1>")


# def verify_phone(request):
#     context = {
#         'error_message': '', 
#         'info': ''
#     }
#     if request.method == "POST":
#         if 'resend' in request.POST:
#             for l in list(OneTimePassword.objects.filter(user=request.user, type=1)):
#                 l.delete()
#             time=datetime.datetime.now()
#             time_sec = str((int(time.year) * 31536000) + (int(time.month) * 2592000) + (int(time.day) * 86400) + (int(time.hour) * 3600) + (int(time.minute) * 60) + (int(time.second)))
#             o = OneTimePassword.objects.create(otp=OTP(), user=request.user, time=time_sec, type=1)
#             o.save()
#             send_code(o.otp, phone)


#         else:
#             code = request.POST['code']
#             l = OneTimePassword.objects.get(user=request.user, type=1)
#             now = datetime.datetime.now()
#             then_sec = int(l.time)
#             sec = (int(now.year) * 31536000) + (int(now.month) * 2592000) + (int(now.day) * 86400) + (int(now.hour) * 3600) + (int(now.minute) * 60) + (int(now.second))
#             if sec - then_sec < 1800:
#                 if code == l.otp:
#                     l.delete()
#                     c = CustomUser.objects.get(user=request.user)
#                     c.phone_verified = True
#                     c.save()
#                     return redirect('home')
#                 else:
#                     context['error_message'] = 'Code is invalid.'
#             else:
#                 l.delete()
#                 context['error_message'] = 'The code has expired.'
#                 time=datetime.datetime.now()
#                 time_sec = str((int(time.year) * 31536000) + (int(time.month) * 2592000) + (int(time.day) * 86400) + (int(time.hour) * 3600) + (int(time.minute) * 60) + (int(time.second)))
#                 on = OneTimePassword.objects.create(otp=OTP(), user=request.user, time=time_sec, type=1)
#                 on.save()
#                 send_code(on.otp, phone)
            

#     if (request.user.is_authenticated) and ((CustomUser.objects.get(user=request.user).email_verified == True) and (CustomUser.objects.get(user=request.user).phone_verified == False)):
#         phone = CustomUser.objects.get(user=request.user).phone
#         try:
#             l = OneTimePassword.objects.get(user=request.user, type=1)
#             then_sec = int(l.time)
#             time=datetime.datetime.now()
#             time_sec = str((int(time.year) * 31536000) + (int(time.month) * 2592000) + (int(time.day) * 86400) + (int(time.hour) * 3600) + (int(time.minute) * 60) + (int(time.second)))
#             phone = CustomUser.objects.get(user=request.user).phone
#             if time_sec - then_sec >= 1800:
#                 l.delete()
#                 o = OneTimePassword.objects.create(otp=OTP(), user=request.user, time=time_sec, type=1)
#                 o.save()
#                 send_code(o.otp, phone)
#             else:
#                 context['info'] = "The code we sent you is still valid"
#         except ObjectDoesNotExist:
#             time=datetime.datetime.now()
#             time_sec = str((int(time.year) * 31536000) + (int(time.month) * 2592000) + (int(time.day) * 86400) + (int(time.hour) * 3600) + (int(time.minute) * 60) + (int(time.second)))
#             on = OneTimePassword.objects.create(otp=OTP(), user=request.user, time=time_sec, type=1)
#             on.save()
#             send_code(on.otp, phone)
#         return render(request, 'stux_auth/phone_verification.html')
#     else:
#         return HttpResponse("<h1>You don't have access to this page<h1>")

def logIn(request):
    context = {
        "error_messages": []
    }
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = User.objects.get(email=email)
        u = authenticate(request=request, username=user.username, email=email, password=password)
        if u is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')

        else:
            context['error_messages'].append("Email or Password is invalid")
    return render(request, 'stux_auth/login.html', context=context)

def logOut(request):
    logout(request)
    return redirect('home')


def forgot_password(request):
    context = {
        "error_messages": [], 
        "infos": []
    }
    if request.method == 'POST':
        email = request.POST['email']
        user_id = User.objects.get(email=email).id
        send_mail(
            'Thanks for using my services', 
            request.build_absolute_uri(reverse('change_password', args=(user_id, ))), 
            'unknown@gmail.com', 
            [email], 
            fail_silently=False)
        context['infos'].append("A link has been sent to your email")
    return render(request, 'stux_auth/forgot_password.html', context=context)

def change_password(request, pk):
    context = {
        'error_messages': []
    }

    if request.method == "POST":
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            user = User.objects.get(pk=pk)
            if check_password(password1, user.password):
                context['error_messages'].append("Can't use old password.")
            else:
                user.set_password(password1)
                user.save()
                return redirect('login')
        else:
            context['error_messages'].append('Please make sure both passwords match.')
    return render(request, 'stux_auth/change_password.html', context)


def home(request):
    context = {
        'user': request.user,
        'verified': False,
        'profile_pic': None
    }
    if request.user.is_authenticated:
        email_verified = CustomUser.objects.get(user=request.user).email_verified
        phone_verified = CustomUser.objects.get(user=request.user).phone_verified
        if email_verified:
            context['verified'] = True
        else:
            return redirect('verify')
    return render(request, 'stux_auth/index.html', context)
    
    