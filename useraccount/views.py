from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View, generic
from Books.models import WishList, Book, Feedback, Cart, Contact
from .forms import LoginForm, HyperLinkkForm
from useraccount.forms import RegisterForm, EditForm
from useraccount.models import SimpleUser
from django.views.generic import UpdateView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .forms import EditForm


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


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = SimpleUser
    form_class = EditForm
    template_name = 'users/profile_change.html'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, accepted_order = None, []
        cartitems, orderitems = [], []
        books_page = None
        nums, feedbacks = None, []
        contact = None
        if not self.request.user.is_admin:
            cart, created = WishList.objects.get_or_create(user=self.request.user.simpleuser, completed=False)

            cartitems = cart.wisthlistitems.all().order_by('id')  # Упорядочиваем по полю 'id'

            accepted_order = Cart.objects.filter(user=self.request.user.simpleuser, completed=True).first()
            print(accepted_order)

            if accepted_order != None:
                orderitems = accepted_order.cartitems.all()

            p = Paginator(cartitems, 1)  # Измените число на желаемый размер страницы
            page = self.request.GET.get('page')
            books_page = p.get_page(page)
            nums = "a" * books_page.paginator.num_pages

            feedbacks = Feedback.objects.filter(author_id=self.request.user.simpleuser)

        context['contact'] = contact
        context['orderitems'] = orderitems
        context['accepted_order'] = accepted_order
        context['cart'] = cart
        context['items'] = cartitems
        context['nums'] = nums
        context['books_page'] = books_page
        context['feedbacks'] = feedbacks
        return context


@method_decorator(login_required, name="dispatch")
class SignOut(View):
    def get(self, request):
        logout(request)
        messages.success(request, f'You have been logged out.')
        return redirect('register')


class SignIn(View):
    template_name = 'users/login.html'
    form_class = LoginForm

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
                return redirect('authenticated')

        messages.error(request, f'Invalid username or password')
        return render(request, self.template_name, {'form': form})


class SignUpView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('authenticated')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('authenticated')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        # user.username = user.username.lower()
        user.save()
        messages.success(self.request, 'You have signed up successfully.')
        login(self.request, user)
        return response
