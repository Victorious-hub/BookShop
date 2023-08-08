from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from Books.models import WishList, Book, Feedback
from .forms import LoginForm, HyperLinkkForm
from useraccount.forms import RegisterForm, EditForm
from useraccount.models import SimpleUser


@login_required
def add_hyperlinks(request, id):
    profile = SimpleUser.objects.get(id=id)

    if request.method == 'GET':
        context = {'form': HyperLinkkForm(instance=profile), 'id': id}
        return render(request, 'users/profile_change.html', context)

    elif request.method == 'POST':
        form = HyperLinkkForm(request.POST or None, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('main')
        else:
            return render(request, 'users/profile_change.html', {'form': form})

@login_required
def edit_profile(request, slug):
    profile = get_object_or_404(SimpleUser, slug=slug)

    cart = None
    cartitems = []
    books_page = None
    nums, feedbacks = None, []
    if request.user.is_authenticated and not request.user.is_admin:
        cart, created = WishList.objects.get_or_create(user=request.user.simpleuser, completed=False)
        cartitems = cart.wisthlistitems.all()

        p = Paginator(cart.wisthlistitems.all(), 1)

        page = request.GET.get('page')

        books_page = p.get_page(page)

        nums = "a" * books_page.paginator.num_pages

        feedbacks = Feedback.objects.filter(author_id=request.user.simpleuser)

    if request.method == 'GET':
        context = {
            'form': EditForm(instance=profile),
            'slug': slug,
            "cart": cart,
            "items": cartitems,
            "nums": nums,
            "books_page": books_page,
            "feedbacks": feedbacks
        }
        return render(request, 'users/profile_change.html', context)

    elif request.method == 'POST':
        form = EditForm(request.POST or None, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('main')
        else:
            return render(request, 'users/profile_change.html', {'form': form})

@login_required
def sign_out(request):
    logout(request)
    messages.success(request, f'You have been logged out.')
    return redirect('register')


def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = request.POST.get('email')
        print(email)
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


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('authenticated')

    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})

    elif request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            # user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have signed up successfully.')
            login(request, user)
            return redirect('authenticated')
        else:
            return render(request, 'users/register.html', {'form': form})
