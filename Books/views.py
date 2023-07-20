import json
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from django.db.models import Q
from .models import Book, SimpleUser, CartItem, Cart, Feedback
from . import serializer
from . import models
from .forms import RegisterForm, LoginForm, BookForm, EditForm, FeedbackForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt


def cart(request):
    cart = None
    cartitems = []
    if request.user.is_authenticated and not request.user.is_admin:
        cart, created = Cart.objects.get_or_create(user=request.user.simpleuser, completed=False)
        cartitems = cart.cartitems.all()
    context = {"cart": cart, "items": cartitems}
    return render(request, 'users/cart.html', context)


def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = Book.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user.simpleuser, completed=False)

        cartitem, created = CartItem.objects.get_or_create(cart=cart, book_product=product)

        cartitem.quantity += 1

        cartitem.save()

        num_of_item = cart.num_of_items

        print(cartitem)
    return JsonResponse("Working", safe=False)


def remove_from_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = Book.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user.simpleuser, completed=False)

        cartitem, created = CartItem.objects.get_or_create(cart=cart, book_product=product)

        cartitem.quantity -= 1
        if cartitem.quantity == 0:
            cartitem.delete()
        else:
            cartitem.save()
        num_of_item = cart.num_of_items

        print("Deleted")
    return JsonResponse({'price': cartitem.price, 'num_of_items': num_of_item}, safe=False)


def remove_all(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = Book.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user.simpleuser, completed=False)

        cartitem, created = CartItem.objects.get_or_create(cart=cart, book_product=product)

        cartitem.delete()

        num_of_item = cart.num_of_items

        print("Deleted")
    return JsonResponse({'price': cartitem.price, 'num_of_items': num_of_item}, safe=False)


def main(request):
    books = Book.objects.all()

    p = Paginator(Book.objects.all(), 2)
    page = request.GET.get('page')
    books_page = p.get_page(page)
    if request.user.is_authenticated and not request.user.is_admin:
        cart, created = Cart.objects.get_or_create(user=request.user.simpleuser, completed=False)
    context = {'books': books, 'books_page': books_page, }
    return render(request, 'users/base.html', context)


@login_required
def authenticated(request):
    books = Book.objects.all()

    p = Paginator(Book.objects.all(), 2)
    page = request.GET.get('page')
    books_page = p.get_page(page)
    if request.user.is_authenticated and not request.user.is_admin:
        cart, created = Cart.objects.get_or_create(user=request.user.simpleuser, completed=False)
    context = {'books': books, 'books_page': books_page, }
    return render(request, 'users/authenticated.html', context)


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
            return redirect('authenticated')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request, 'books/add_book.html', {'form': form})


@login_required
def add_feedback(request, id):
    books = Book.objects.get(id=id)

    if request.method == 'GET':
        context = {'form': FeedbackForm(instance=books), 'id': id}
        return render(request, 'Feedback/add_feedback.html', context)


    elif request.method == 'POST':

        form = FeedbackForm(request.POST, request.FILES)

        if form.is_valid():

            feedback = form.save(commit=False)

            feedback.author = request.user.simpleuser

            feedback.book_id = books  # Установите значение book_id

            feedback.save()

            return redirect('authenticated')

        else:

            messages.error(request, 'Please correct the following errors:')

            return render(request, 'Feedback/add_feedback.html', {'form': form})


@login_required
def feedbacks(request, id):
    books = Book.objects.get(id=id)
    feedbacks = Feedback.objects.filter(book_id=books)
    context = {'feedbacks': feedbacks}
    return render(request, 'Feedback/feedbacks.html', context)
