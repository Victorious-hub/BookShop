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
from useraccount.forms import RegisterForm, LoginForm, EditForm, HyperLinkkForm
from useraccount.models import SimpleUser


class AddHyperlinksView(LoginRequiredMixin, UpdateView):
    model = SimpleUser
    form_class = HyperLinkkForm
    template_name = "users/profileChange.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("main")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["id"] = self.kwargs["id"]
        return context


class ChangePasswordView(LoginRequiredMixin, View):
    model = SimpleUser
    template_name = "users/profileChange.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy("register")

    def post(self, request):
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
    model = SimpleUser
    form_class = EditForm
    template_name = "users/profileChange.html"
    slug_url_kwarg = "slug"
    slug_field = "slug"
    success_url = reverse_lazy("main")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_admin:
            cart, created = WishList.objects.get_or_create(user=self.request.user.simpleuser, completed=False)

            cart_items = cart.wisthlistitems.all().order_by("id")

            accepted_order = Cart.objects.filter(user=self.request.user.simpleuser, completed=True).first()

            if accepted_order is not None:
                order_items = accepted_order.cartitems.all()
                context["order_items"] = order_items

            p = Paginator(cart_items, 1)
            page = self.request.GET.get("page")
            books_page = p.get_page(page)
            nums = "a" * books_page.paginator.num_pages
            feedbacks = Feedback.objects.filter(author_id=self.request.user.simpleuser)

            context["contact"] = None
            context["accepted_order"] = accepted_order
            context["cart"] = cart
            context["items"] = cart_items
            context["nums"] = nums
            context["books_page"] = books_page
            context["feedbacks"] = feedbacks
        return context


class SignOut(LoginRequiredMixin, View):
    success_url = reverse_lazy("register")

    def get(self, request):
        logout(request)
        return redirect(self.success_url)


class SignIn(View):
    template_name = "users/register.html"
    form_class = LoginForm
    success_url = reverse_lazy("tovar_page")

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )
            if user:
                login(request, user)
                return redirect(self.success_url)

        return render(request, self.template_name, {"form": form})


class SignUpView(CreateView):
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("tovar_page")

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
        messages.error(self.request, "Invalid submission.")
        return super().form_invalid(form)