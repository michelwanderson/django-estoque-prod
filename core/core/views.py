# core/views.py (ou accounts/views.py)
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('menu')
        else:
            messages.error(request, 'Usuário ou senha inválidos')

    return render(request, 'core/login.html')



@login_required(login_url='login')
def menu(request):
    return render(request, 'core/menu.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
