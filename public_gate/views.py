from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def home(request):
    d = {}
    return render(request, 'home.html', d)


def about(request):
    d = {}
    return render(request, 'about.html', d)


def contact(request):
    d = {}
    return render(request, 'contact.html', d)


def site_login(request):
    if request.method == "POST":
        user_login = request.POST['login']
        user_password = request.POST['password']
        user = authenticate(username=user_login, password=user_password)
        if user is not None:
            login(request, user)
            return render(request, 'home.html')
        else:
            # User.objects.create_user(user_login, '', user_password).save()
            return render(request, 'home.html', {"error_message": "Wrong login/password combination"})
    return render(request, 'home.html', {"error_message": "One or more fields are empty"})


def site_logout(request):
    logout(request)
    return render(request, 'home.html')