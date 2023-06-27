from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login, authenticate, logout
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from .models import Book
from .serializer import UserSerializer
from . import models
from .forms import RegisterForm, LoginForm, BookForm

from django.contrib import messages


def main(request):
    posts = Book.objects.all()
    context = {'posts': posts}
    return render(request, 'users/base.html', context)


def sign_out(request):
    logout(request)
    messages.success(request, f'You have been logged out.')
    return redirect('login')


class sign_in(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('main')

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
                return redirect('main')

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
            return redirect('main')
        else:
            return render(request, 'users/register.html', {'form': form})


class UserRestSignUp(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]

    queryset = models.SimpleUser.objects.all()
    serializer_class = UserSerializer


@login_required
def delete_book(request, id):
    queryset = Book.objects.filter(author=request.user)
    post = get_object_or_404(queryset, pk=id)
    context = {'post': post}

    if request.method == 'GET':
        return render(request, 'books/add_book.html', context)
    elif request.method == 'POST':
        post.delete()
        messages.success(request, 'The post has been deleted successfully.')
        return redirect('main')
@login_required
def edit_book(request, id):
    queryset = Book.objects.filter(author=request.user)
    post = get_object_or_404(queryset, pk=id)

    if request.method == 'GET':
        context = {'form': BookForm(instance=post), 'id': id}
        return render(request, 'books/add_book.html', context)

    elif request.method == 'POST':
        form = BookForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been updated successfully.')
            return redirect('main')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request, 'books/add_book.html', {'form': form})


@login_required
def add_book(request):
    if request.method == 'GET':
        context = {'form': BookForm()}
        return render(request, 'books/add_book.html', context)
    elif request.method == 'POST':
        form = BookForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.author = request.user
            user.save()
            messages.success(request, 'The post has been created successfully.')
            return redirect('main')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request, 'books/add_book.html', {'form': form})