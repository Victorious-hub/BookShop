import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DeleteView, UpdateView, CreateView, DetailView
from elasticsearch_dsl import Q
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .forms import BookForm, FeedbackForm, ContactForm
from .models import Book, CartItem, Cart, Feedback, WishList, WisthlistItem


class CreatePDFView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        book = Book.objects.get(id=id)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="BookReview.pdf"'
        pdf = canvas.Canvas(response, pagesize=letter)

        title_font_size = 16
        content_font_size = 12
        page_width, page_height = letter

        title = book.book_name

        pdf.setFont("Helvetica-Bold", title_font_size)
        pdf.drawCentredString(page_width / 2, page_height - 50, title)

        pdf.setFont("Helvetica", content_font_size)
        textobject = pdf.beginText(50, page_height - 100)
        textobject.setFont("Helvetica", content_font_size)
        textobject.setTextOrigin(50, page_height - 100)

        text = """
            Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
            Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis
            dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec,
            pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, 
            fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, 
            venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus.
            Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
            Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis
            dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec,
            pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, 
            fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, 
            venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus.
            Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
            Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis
            dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec,
            pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, 
            fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, 
            venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus.
            Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
            Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis
            dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec,
            pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, 
            fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, 
            venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus.
            Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
            Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis
            dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec,
            pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, 
            fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, 
            venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus.
            Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
            Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis
            dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec,
            pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, 
            fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, 
            venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus.
            Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
            Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis
            dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec,
            pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, 
            fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, 
            venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus.
            """

        lines = text.splitlines()
        for line in lines:
            textobject.textLine(line)

        pdf.drawText(textobject)

        # Add page 2
        pdf.showPage()

        pdf.setFont("Helvetica-Bold", title_font_size)

        pdf.setFont("Helvetica", content_font_size)
        textobject = pdf.beginText(50, page_height - 100)
        textobject.setFont("Helvetica", content_font_size)
        textobject.setTextOrigin(50, page_height - 100)

        for line in lines:
            textobject.textLine(line)

        pdf.drawText(textobject)

        pdf.showPage()
        pdf.save()

        return response


class CartView(LoginRequiredMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cart = None
        self.cartitems = None

    def get(self, request):
        self.cart = None
        self.cartitems = []
        if request.user.is_authenticated and not request.user.is_admin:
            self.cart, created = Cart.objects.get_or_create(user=request.user.simpleuser, completed=False)
            self.cartitems = self.cart.cartitems.all()
        context = {"cart": self.cart, "items": self.cartitems}
        return render(request, 'Cart/CartTest.html', context)


class AddToCartView(LoginRequiredMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = None
        self.cartitem = None
        self.cart = None
        self.num_of_item = None

    model = Book
    cart_model = Cart
    cartitem_model = CartItem

    def post(self, request):
        data = json.loads(request.body)
        product_id = data["id"]
        self.product = self.model.objects.get(id=product_id)
        self.cart, created = self.cart_model.objects.get_or_create(user=request.user.simpleuser, completed=False)

        self.cartitem, created = self.cartitem_model.objects.get_or_create(cart=self.cart, book_product=self.product)

        self.cartitem.quantity += 1

        self.cartitem.save()

        num_of_item = self.cart.num_of_items

        return JsonResponse({'price': self.cartitem.price, 'num_of_items': num_of_item}, safe=False)


class RemoveFromCart(LoginRequiredMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = None
        self.cartitem = None
        self.cart = None
        self.num_of_item = None

    model = Book
    cart_model = Cart
    cartitem_model = CartItem

    def post(self, request):
        data = json.loads(request.body)
        product_id = data["id"]
        self.product = self.model.objects.get(id=product_id)
        self.cart, created = self.cart_model.objects.get_or_create(user=request.user.simpleuser, completed=False)
        self.cartitem, created = self.cartitem_model.objects.get_or_create(cart=self.cart, book_product=self.product)

        self.cartitem.quantity -= 1
        if self.cartitem.quantity <= 0:
            self.cartitem.delete()
        else:
            self.cartitem.save()

        self.num_of_item = self.cart.num_of_items

        return JsonResponse({'price': self.cartitem.price, 'num_of_items': self.num_of_item}, safe=False)


class RemoveAllCartView(LoginRequiredMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = None
        self.cartitem = None
        self.cart = None
        self.num_of_item = None

    model = Book
    cart_model = Cart
    cartitem_model = CartItem
    def post(self, request, id):
        data = json.loads(request.body)
        product_id = data["id"]
        self.product = self.model.objects.get(id=product_id)

        if request.user.is_authenticated:
            self.cart_model, created = Cart.objects.get_or_create(user=request.user.simpleuser, completed=False)

            self.cartitem_model, created = CartItem.objects.get_or_create(cart=self.cart, book_product=self.product)

            self.cartitem_model.delete()

            self.num_of_item = self.cart.num_of_items

        return JsonResponse({'price': self.cartitem.price, 'num_of_items': self.num_of_item}, safe=False)


class Main(TemplateView):
    template_name = 'users/main.html'


class BookDetailView(LoginRequiredMixin, DetailView):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.id = None
        self.book = None
        self.feedbacks = None

    model = Book
    feedback_model = Feedback
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get(self, request, *args, **kwargs):
        self.id = kwargs.get('id')
        self.book = self.model.objects.get(id=id)
        self.feedbacks = self.feedback_model.objects.filter(book_id=self.book)
        context = {'book': self.book, 'feedbacks': self.feedbacks}
        return render(request, self.template_name, context)


class AuthenticatedView(LoginRequiredMixin, TemplateView):
    model = Book
    template_name = 'users/tovar_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.model.objects.all()

        p = Paginator(Book.objects.all(), 6)
        page = self.request.GET.get('page')

        books_page = p.get_page(page)

        context['books_page'] = books_page
        context['nums'] = "a" * books_page.paginator.num_pages
        if self.request.user.is_authenticated and not self.request.user.is_admin:
            cart, created = Cart.objects.get_or_create(user=self.request.user.simpleuser, completed=False)
        return context


class BookDeleteView(LoginRequiredMixin, DeleteView):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.object = None

    model = Book
    success_url = reverse_lazy("main")
    template_name = "books/delete_book.html"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())
        else:
            raise Http404


class SearchBooksView(LoginRequiredMixin, View):
    model = Book
    template_name = ["books/search_book.html", "users/main.html"]

    def post(self, request):
        searched = request.POST["searched"]
        if len(searched) != 0:
            book_names = Book.objects.filter(Q(book_name__contains=searched) | Q(book_author__contains=searched))
            return render(request, self.template_name[0], {"searched": searched, "book_names": book_names, })
        else:
            return render(request, self.template_name[1], {})


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/edit-book.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CreateBookView(LoginRequiredMixin, CreateView):
    form_class = BookForm
    template_name = "books/add_book.html"
    success_url = reverse_lazy("tovar_page")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AddFeedBackView(LoginRequiredMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.feedbacks = None
        self.books = None
        self.id = None
        self.feedback = None

    model = Book
    feedback_model = Feedback
    template_name = 'Feedback/add_feedback.html'
    form_class = FeedbackForm

    def get(self, request, *args, **kwargs):
        self.id = kwargs.get('id')
        self.books = self.model.objects.get(id=self.id)
        self.feedbacks = self.feedback_model.objects.filter(book_id=self.books)
        context = {'form': self.form_class(instance=self.books), 'id': self.id}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self.id = kwargs.get('id')
        self.books = self.model.objects.get(id=self.id)
        self.feedbacks = self.feedback_model.objects.filter(book_id=self.books)
        if len(self.feedbacks) == 0:
            form = self.form_class(request.POST)
            if form.is_valid():
                self.feedback = form.save(commit=False)
                self.feedback.author = request.user.simpleuser
                self.feedback.book_id = self.books
                self.feedback.save()
                return redirect('tovar_page')

            else:
                messages.error(request, 'Please correct the following errors:')
                return render(request, self.template_name, {'form': form})
        return render(request, 'users/tovar_page.html', )


"""class FeedBacksView(LoginRequiredMixin, View):
    def get(self, request, id):
        books = Book.objects.get(id=id)
        feedbacks = Feedback.objects.filter(book_id=books)
        context = {'feedbacks': feedbacks}
        return render(request, 'Feedback/feedbacks.html', context)"""


class CheckersView(LoginRequiredMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.searched = None
        self.year_searched = None
        self.price_min = None
        self.price_max = None
        self.books = None

    model = Book
    template_name = "books/checker.html"

    def post(self, request):
        self.searched = request.POST.getlist('searched')
        self.year_searched = request.POST.getlist('year_searched')
        self.price_min = request.POST.get('priceMin')
        self.price_max = request.POST.get('priceMax')

        filters = {
            'genre__in': self.searched,
            'book_year__in': self.year_searched,
            'price__gte': self.price_min,
            'price__lte': self.price_max,
        }

        books_queryset = self.model.objects.filter(**filters)

        if not any(filters.values()):
            return render(request, 'users/main.html')

        self.books = books_queryset.exclude(**{k: v for k, v in filters.items() if v == '0'})
        context = {'books': self.books}
        return render(request, self.template_name, context)


class AddToWishlistView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = None
        self.cart = None
        self.cartitem = None

    model = Book
    wishlist_model = WishList
    wishlistitem_model = WisthlistItem

    def post(self, request):
        data = json.loads(request.body)
        product_id = data["id"]
        self.product = self.model.objects.get(id=product_id)

        if request.user.is_authenticated:
            self.cart, created = self.wishlist_model.objects.get_or_create(user=request.user.simpleuser,
                                                                           completed=False)
            self.cart.save()
            self.cartitem, created = self.wishlistitem_model.objects.get_or_create(wisthlist_item=self.cart,
                                                                                   book_product=self.product)

            self.cartitem.quantity += 1
            self.cartitem.save()
        return JsonResponse("Working", safe=False)


class RemoveWishList(LoginRequiredMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = None
        self.cart = None
        self.cartitem = None

    model = Book
    wishlist_model = WishList
    wishlistitem_model = WisthlistItem

    def post(self, request):
        data = json.loads(request.body)
        product_id = data["id"]
        self.product = self.model.objects.get(id=product_id)

        if request.user.is_authenticated:
            self.cart, created = self.wishlist_model.objects.get_or_create(user=request.user.simpleuser,
                                                                           completed=False)
            self.cart.save()

            self.cartitem, created = self.wishlistitem_model.objects.get_or_create(wisthlist_item=self.cart,
                                                                                   book_product=self.product)

            self.cartitem.quantity -= 1
            self.cartitem.remove()
        return JsonResponse("Working", safe=False)


class AcceptContact(LoginRequiredMixin, View):
    model = Cart
    template_name = 'Payment/Contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('main')

    def get(self, request):
        form = ContactForm(request.GET)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')

        subject = "Hey, dude"
        message = f"Hi {first_name}, you have accepted your purchase"
        email_from = settings.EMAIL_HOST_USER

        form = self.form_class(request.POST)
        try:
            cart = self.model.objects.get(user=request.user.simpleuser, completed=False)
        except self.model.DoesNotExist:
            return HttpResponseRedirect('cart')

        ordered_books = []
        cart_items = cart.cartitems.all()
        for cart_item in cart_items:
            ordered_books.append(cart_item)

        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user.simpleuser
            contact.save()
            cart.completed = True

            contact.ordered_books.set(ordered_books)

            cart.save()

            send_mail(subject, message, email_from, [email])
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})


class DeleteFeedBackView(LoginRequiredMixin, DetailView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = None
        self.books = None
        self.feedbacks = None

    model = Book
    feedback_model = Feedback
    success_url = reverse_lazy('main')
    template_name = 'users/profile_change.html'

    def get(self, request, *args, **kwargs):
        self.id = kwargs.get('id')
        self.books = self.model.objects.get(id=id)
        self.feedbacks = self.feedback_model.objects.filter(book_id=self.books).delete()

        messages.success(request, 'The post has been deleted successfully.')
        return redirect(self.success_url)


class EditFeedbackView(LoginRequiredMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = None
        self.books = None
        self.feedbacks = None

    model = Book
    feedback_model = Feedback
    template_name = 'users/profile_change.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('main')

    def get(self, request, *args, **kwargs):
        self.id = kwargs.get('id')
        self.books = self.model.objects.get(id=self.id)
        self.feedbacks = self.feedback_model.objects.filter(book_id=self.books)
        context = {'feedbacks': self.feedbacks, 'id': self.id}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self.books = self.model.objects.get(id=id)
        self.feedbacks = self.feedback_model.objects.filter(book_id=self.books)
        form = self.form_class(request.POST or None, instance=self.feedbacks.first())
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been updated successfully.')
            return redirect(self.success_url)
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request, self.template_name, {'form': form})
