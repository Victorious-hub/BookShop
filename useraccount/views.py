from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.contrib import messages
from .forms import LoginForm
from useraccount.forms import RegisterForm, EditForm
from useraccount.models import SimpleUser


@login_required
def edit_profile(request, id):
    profile = SimpleUser.objects.get(id=id)

    if request.method == 'GET':
        context = {'form': EditForm(instance=profile), 'id': id}
        return render(request, 'users/edit_profile.html', context)

    elif request.method == 'POST':
        form = EditForm(request.POST or None, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('main')
        else:
            return render(request, 'users/edit_profile.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, f'You have been logged out.')
    return redirect('login')


class sign_in(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('authenticated')

        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {email.title()}, welcome back!')
                return redirect('authenticated')

        messages.error(request, f'Invalid username or password')
        return render(request, 'users/login.html', {'form': form})


class sign_up(APIView):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('authenticated')
        else:
            return render(request, 'users/register.html', {'form': form})
