from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm

# Registration view
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Automatically log the user in
            return redirect('home')  # Redirect to home page after registration
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


# In shop/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
