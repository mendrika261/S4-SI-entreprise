from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .tools import *


@logout_required
def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            context['username'] = username
            context['errors'] = 'Mot de passe incorrect'

    return render(request, 'user/login.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
