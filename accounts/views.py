from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils import timezone
# Create your views here.


def register(request):
    if request.user.is_authenticated:
        return redirect('/accounts/index')
        
    message = ""
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2 and len(password1) >= 8:
            if User.objects.filter(username = username).exists():
                print("username exists.")
                message = 1
                messages.info(request, "username exists.")
            elif User.objects.filter(email=email).exists():
                print("email already exists.")
                message = 1
                messages.info(request, "email already exists.")
            else:
                user = User.objects.create_user(username = username, password = password1, email = email, last_name = last_name, first_name = first_name).save()
        elif password1 != password2:
            print("password not maching..")
            message = 1
            messages.info(request, "password not maching..")
        else:
            print("password is weak. Please check password policy!")
            message = 1
            messages.info(request, "password is weak. Please check password policy!")


        if message:
            return redirect('/accounts/register')
        else:
            return redirect('/accounts/index')

    else:
        return render(request, 'register.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('/accounts/index')

    message = ""
    context = {}
    try:
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            username = User.objects.get(email=email.lower()).username
            user = auth.authenticate(username = username, password = password)
            print(user)

            if user:
                login(request, user)
                if request.GET.get('next', None):
                    return HttpResponseRedirect(request.GET['next'])
                else:
                    return redirect('/accounts/home')
            else:
                print("email or password is worng!")
                message = 1
                messages.info(request, "email or password is worng!")
                return redirect('/accounts/login')
        else:
            return render(request, 'login.html')
    except:
            print("email or password is worng!")
            message = 1
            messages.info(request, "email or password is worng!")
            return redirect('/accounts/login')

@login_required(login_url = '/accounts/login')
def index(request):
    details = User.objects.all()
    return render(request, 'index.html', {'details': details})

#@login_required()
def home(request):
    return render(request, 'home.html')

def user_logout(request, *args, **kwargs):
    user = request.user
    #profile = user.get_profile()
    #profile.last_logout = timezone.now()
    #profile.save()
    logout(request, *args, **kwargs)
    return render(request, 'home.html')
