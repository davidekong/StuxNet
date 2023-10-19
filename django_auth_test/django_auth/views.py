from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def register(request):
    context = {
        "error_message": ''
    }
    if request.method == "POST":
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            try:
                User.objects.get(email=email)
                context['error_message'] = 'Email already exists'
            except ObjectDoesNotExist:
                user = User.objects.create_user('user', email, password1)
                user.username = f'user{user.id}'
                user.save()
                login(request, user)
                return redirect('home')
        else:
            context['error_message'] = 'Password does not match'

    return render(request, 'django_auth/register.html', context)

def extra_info(request):
    

def landing_page(request):
    context = {
        'user': request.user,
    }
    return render(request, 'django_auth/landing_page.html', context)