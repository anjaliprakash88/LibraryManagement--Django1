from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib import messages


def login_form(request):
    return render(request, 'bookstore/login.html')


def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:  # user account is active or not
            auth.login(request,
                       user)  # This function is responsible for setting the necessary session data to keep the user logged in.
            if user.is_admin or user.is_superuser:
                return redirect('dashboard')
            elif user.is_librarian:
                return redirect("librarian")
            else:
                return redirect('publisher')
        else:
            messages.info(request, "invalid username and password")
            return redirect('home')





def publisher(request):
    return render(request, 'publisher/home.html')


def librarian(request):
    return render(request, 'librarian/home.html')


def dashboard(request):
    return render(request, 'dashboard/home.html')