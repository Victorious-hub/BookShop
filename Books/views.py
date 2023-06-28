from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from django.db.models import Q
from .models import Book, SimpleUser
from . import serializer
from . import models
from .forms import RegisterForm, LoginForm, BookForm, EditForm
from django.contrib import messages


def main(request):
    books = Book.objects.all()
    context = {'books': books}
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


class ProfileListView(generics.ListCreateAPIView):
    queryset = models.SimpleUser.objects.all()
    serializer_class = serializer.UserSerializer


class ProfileChange(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SimpleUser.objects.all()
    serializer_class = serializer.UserSerializer


@login_required
def delete_book(request, id):
    permission_classes = [IsAdminUser]
    book = Book.objects.get(id=id)
    context = {'post': book}

    if request.method == 'GET':
        return render(request, 'books/delete_book.html', context)
    elif request.method == 'POST':
        book.delete()
        messages.success(request, 'The post has been deleted successfully.')
        return redirect('main')


def search_books(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        book_names = Book.objects.filter(Q(book_name__contains=searched) | Q(book_author__contains=searched))
        return render(request, 'books/search_book.html', {'searched': searched, 'book_names': book_names, })
    else:
        return render(request, 'books/search_book.html', {})


@login_required
def edit_book(request, id):
    permission_classes = [IsAdminUser]
    book = Book.objects.get(id=id)

    if request.method == 'GET':
        context = {'form': BookForm(instance=book), 'id': id}
        return render(request, 'books/edit-book.html', context)

    elif request.method == 'POST':
        form = BookForm(request.POST or None, request.FILES or None, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been updated successfully.')
            return redirect('main')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request, 'books/edit-book.html', {'form': form})


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


@login_required
def add_book(request):
    permission_classes = [IsAdminUser]
    if request.method == 'GET':
        context = {'form': BookForm()}
        return render(request, 'books/add_book.html', context)
    elif request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.author = request.user
            user.save()
            return redirect('main')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request, 'books/add_book.html', {'form': form})
