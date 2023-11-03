from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, CreateView

from Books.models import WishList, Feedback, Cart
from useraccount.forms import RegisterForm
from useraccount.models import SimpleUser
from .forms import EditForm
from .forms import LoginForm, HyperLinkkForm


class AddHyperlinksView(LoginRequiredMixin, UpdateView):
    model = SimpleUser
    form_class = HyperLinkkForm
    template_name = 'users/profile_change.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context


class ChangePasswordView(LoginRequiredMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = None
        self.id = None

    model = SimpleUser
    template_name = "users/profile_change.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy("register")

    def post(self, request, *args, **kwargs):
        self.id = kwargs.get("id")
        self.profile = self.model.objects.get(id=self.id)
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect(self.success_url)
        else:
            messages.error(request, "Please correct the error below.")
        return render(request, self.template_name, {"form": form})


class EditProfileView(LoginRequiredMixin, UpdateView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cart = None
        self.accepted_order = []
        self.cartitems = []
        self.orderitems = []
        self.books_page = None
        self.nums = None
        self.feedbacks = []
        self.contact = None

    model = SimpleUser
    form_class = EditForm
    template_name = 'users/profile_change.html'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_admin:
            self.cart, created = WishList.objects.get_or_create(user=self.request.user.simpleuser, completed=False)

            self.cartitems = self.cart.wisthlistitems.all().order_by('id')

            self.accepted_order = Cart.objects.filter(user=self.request.user.simpleuser, completed=True).first()

            if self.accepted_order is not None:
                self.orderitems = self.accepted_order.cartitems.all()

            p = Paginator(self.cartitems, 1)  # Измените число на желаемый размер страницы
            page = self.request.GET.get('page')
            self.books_page = p.get_page(page)
            self.nums = "a" * self.books_page.paginator.num_pages
            self.feedbacks = Feedback.objects.filter(author_id=self.request.user.simpleuser)

        context["contact"] = self.contact
        context["orderitems"] = self.orderitems
        context["accepted_order"] = self.accepted_order
        context["cart"] = self.cart
        context["items"] = self.cartitems
        context["nums"] = self.nums
        context["books_page"] = self.books_page
        context["feedbacks"] = self.feedbacks
        return context


class SignOut(LoginRequiredMixin, View):
    success_url = reverse_lazy("register")

    def get(self, request):
        logout(request)
        messages.success(request, f"You have been logged out.")
        return redirect(self.success_url)


class SignIn(View):
    template_name = 'users/register.html'
    form_class = LoginForm
    success_url = reverse_lazy("tovar_page")

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect(self.success_url)

        messages.error(request, f"Invalid username or password")
        return render(request, self.template_name, {'form': form})


class SignUpView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('tovar_page')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        user.save()
        messages.success(self.request, "You have signed up successfully.")
        login(self.request, user)
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Invalid form submission. Please check the entered values.")
        return super().form_invalid(form)
