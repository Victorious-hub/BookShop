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
from django.db.models import Q
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .forms import BookForm, FeedbackForm, ContactForm
from .models import Book, CartItem, Cart, Feedback, WishList, WisthlistItem


class CreatePDFView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        book = Book.objects.get(id=kwargs.get("id"))

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename='BookReview.pdf'"
        pdf = canvas.Canvas(response, pagesize=letter)

        title_font_size = 16
        content_font_size = 12
        page_width, page_height = letter

        title = book.book_name

        pdf.setFont("Helvetica-Bold", title_font_size)
        pdf.drawCentredString(page_width / 2, page_height - 50, title)

        pdf.setFont("Helvetica", content_font_size)
        text_object = pdf.beginText(50, page_height - 100)
        text_object.setFont("Helvetica", content_font_size)
        text_object.setTextOrigin(50, page_height - 100)

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
            interpellates eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, 
            flavoring vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, 
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
            text_object.textLine(line)

        pdf.drawText(text_object)

        # Add page 2
        pdf.showPage()

        pdf.setFont("Helvetica-Bold", title_font_size)

        pdf.setFont("Helvetica", content_font_size)
        text_object = pdf.beginText(50, page_height - 100)
        text_object.setFont("Helvetica", content_font_size)
        text_object.setTextOrigin(50, page_height - 100)

        for line in lines:
            text_object.textLine(line)

        pdf.drawText(text_object)

        pdf.showPage()
        pdf.save()

        return response


class CartView(LoginRequiredMixin, View):
    template_name = "Cart/CartTest.html"
    model = Cart

    def get(self, request):
        cart = None
        cart_items = []
        if request.user.is_authenticated and not request.user.is_admin:
            cart, created = self.model.objects.get_or_create(user=request.user.simpleuser, completed=False)
            cart_items = cart.cartitems.all()
        context = {"cart": cart, "items": cart_items}
        return render(request, self.template_name, context)


class AddToCartView(LoginRequiredMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cart_item = None
        self.num_of_item = None

    model = Book
    cart_model = Cart
    cart_item_model = CartItem

    def post(self, request):
        data = json.loads(request.body)
        product_id = data["id"]
        product = self.model.objects.get(id=product_id)
        cart, created = self.cart_model.objects.get_or_create(user=request.user.simpleuser, completed=False)

        self.cart_item, created = self.cart_item_model.objects.get_or_create(cart=cart, book_product=product)
        self.cart_item.quantity += 1
        self.cart_item.save()
        self.num_of_item = cart.num_of_items

        return JsonResponse({"price":  self.cart_item.price, "num_of_items": self.num_of_item}, safe=False)


class RemoveFromCart(LoginRequiredMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cart_item = None
        self.num_of_item = None

    model = Book
    cart_model = Cart
    cart_item_model = CartItem

    def post(self, request):
        data = json.loads(request.body)
        product_id = data["id"]
        product = self.model.objects.get(id=product_id)
        cart, created = self.cart_model.objects.get_or_create(user=request.user.simpleuser, completed=False)
        self.cart_item, created = self.cart_item_model.objects.get_or_create(cart=cart, book_product=product)

        self.cart_item.quantity -= 1
        if self.cart_item.quantity <= 0:
            self.cart_item.delete()
        else:
            self.cart_item.save()
        self.num_of_item = cart.num_of_items

        return JsonResponse({"price": self.cart_item.price, "num_of_items": self.num_of_item}, safe=False)


class RemoveAllCartView(LoginRequiredMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cart_item = None
        self.num_of_item = None

    model = Book
    cart_model = Cart
    cart_item_model = CartItem
    def post(self, request, *args,**kwargs):
        data = json.loads(request.body)
        product_id = data["id"]
        product = self.model.objects.get(id=product_id)

        if request.user.is_authenticated:
            cart, created = self.cart_model.objects.get_or_create(user=request.user.simpleuser, completed=False)
            self.cart_item, created = self.cart_item_model.objects.get_or_create(cart=cart, book_product=product)
            self.cart_item.delete()
            self.num_of_item = cart.num_of_items

        return JsonResponse({"price": self.cart_item.price, "num_of_items": self.num_of_item}, safe=False)


class Main(TemplateView):
    template_name = "users/base.html"


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    feedback_model = Feedback
    template_name = "books/bookDetail.html"
    context_object_name = "book"

    def get(self, request, *args, **kwargs):
        book = self.model.objects.get(id=kwargs.get("id"))
        feedbacks = self.feedback_model.objects.filter(book_id=book)
        context = {"book": book, "feedbacks": feedbacks}
        return render(request, self.template_name, context)


class AuthenticatedView(LoginRequiredMixin, TemplateView):
    model = Book
    template_name = "users/booksPage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.model.objects.all()

        p = Paginator(Book.objects.all(), 6)
        page = self.request.GET.get("page")

        books_page = p.get_page(page)

        context["books_page"] = books_page
        context["nums"] = "a" * books_page.paginator.num_pages
        if self.request.user.is_authenticated and not self.request.user.is_admin:
            _, created = Cart.objects.get_or_create(user=self.request.user.simpleuser, completed=False)
        return context

class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy("main")
    template_name = "books/deleteBook.html"

    def delete(self, request, *args, **kwargs):
        book = self.get_object()
        if book.user == request.user:
            book.delete()
            return HttpResponseRedirect(self.get_success_url())
        else:
            raise Http404


class SearchBooksView(LoginRequiredMixin, View):
    model = Book
    template_book_search_name = "books/searchBook.html"
    template_users_name = "users/base.html"

    def post(self, request):
        searched = request.POST["searched"]
        if len(searched) != 0:
            book_names = self.model.objects.filter(Q(book_name__contains=searched) | Q(book_author__contains=searched))
            return render(request, self.template_book_search_name, {"searched": searched, "book_names": book_names})
        else:
            return render(request, self.template_users_name, {})


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/editBook.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CreateBookView(LoginRequiredMixin, CreateView):
    form_class = BookForm
    template_name = "books/addBook.html"
    success_url = reverse_lazy("tovar_page")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AddFeedBackView(LoginRequiredMixin, View):
    model = Book
    feedback_model = Feedback
    template_add_feedback_name = "Feedback/addFeedback.html"
    template_product_template = "users/booksPage.html"
    form_class = FeedbackForm

    def get(self, request, *args, **kwargs):

        books = self.model.objects.get(id=kwargs.get("id"))
        self.feedback_model.objects.filter(book_id=books)
        context = {"form": self.form_class(instance=books), "id": kwargs.get("id")}
        return render(request, self.template_add_feedback_name, context)

    def post(self, request, *args, **kwargs):

        books = self.model.objects.get(id=kwargs.get("id"))
        feedbacks = self.feedback_model.objects.filter(book_id=books)
        if len(feedbacks) == 0:
            form = self.form_class(request.POST)
            if form.is_valid():
                feedback = form.save(commit=False)
                feedback.author = request.user.simpleuser
                feedback.book_id = books
                feedback.save()
                return redirect("tovar_page")

            else:
                messages.error(request, "Please correct the following errors:")
                return render(request, self.template_add_feedback_name, {"form": form})
        return render(request, self.template_product_template, )

class CheckersView(LoginRequiredMixin, View):
    model = Book
    template_name = "books/checker.html"

    def post(self, request):
        price_min = request.POST.get('priceMin')
        price_max = request.POST.get('priceMax')
        searched = request.POST.getlist('searched')
        books = self.model.objects.filter(Q(genre__in=searched) & Q(price__gte=price_min, price__lte=price_max))
        context = {'books': books}
        return render(request, self.template_name, context)


class AddToWishlistView(View):
    model = Book
    wishlist_model = WishList
    wishlist_item_model = WisthlistItem

    def post(self, request):
        data = json.loads(request.body)
        product_id = data["id"]
        product = self.model.objects.get(id=product_id)

        if request.user.is_authenticated:
            cart, created = self.wishlist_model.objects.get_or_create(user=request.user.simpleuser,
                                                                           completed=False)
            cart.save()
            cart_item, created = self.wishlist_item_model.objects.get_or_create(wisthlist_item=cart,
                                                                                   book_product=product)
            cart_item.quantity += 1
            cart_item.save()
        return JsonResponse("Working", safe=False)


class RemoveWishList(LoginRequiredMixin, View):
    model = Book
    wishlist_model = WishList
    wishlist_item_model = WisthlistItem

    def post(self, request):
        data = json.loads(request.body)
        product_id = data["id"]
        product = self.model.objects.get(id=product_id)

        if request.user.is_authenticated:
            cart, created = self.wishlist_model.objects.get_or_create(user=request.user.simpleuser,
                                                                           completed=False)
            cart.save()
            cart_item, created = self.wishlist_item_model.objects.get_or_create(wisthlist_item=cart,
                                                                                   book_product=product)
            cart_item.quantity -= 1
            cart_item.remove()
        return JsonResponse("Working", safe=False)


class AcceptContact(LoginRequiredMixin, View):
    model = Cart
    template_name = "Payment/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("main")

    def get(self, request):
        form = self.form_class(request.GET)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")

        subject = "Hey, dude"
        message = f"Hi {first_name}, you have accepted your purchase"
        email_from = settings.EMAIL_HOST_USER

        form = self.form_class(request.POST)
        try:
            cart = self.model.objects.get(user=request.user.simpleuser, completed=False)
        except self.model.DoesNotExist:
            return HttpResponseRedirect("cart")

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
            return render(request, self.template_name, {"form": form})


class DeleteFeedBackView(LoginRequiredMixin, DetailView):
    model = Book
    feedback_model = Feedback
    success_url = reverse_lazy("main")
    template_name = "users/profileChange.html"

    def get(self, request, *args, **kwargs):
        books = self.model.objects.get(id=kwargs.get("id"))
        self.feedback_model.objects.filter(book_id=books).delete()

        messages.success(request, "The post has been deleted successfully.")
        return redirect(self.success_url)


class EditFeedbackView(LoginRequiredMixin, View):
    model = Book
    feedback_model = Feedback
    template_name = "users/profileChange.html"
    form_class = FeedbackForm
    success_url = reverse_lazy("main")

    def get(self, request, *args, **kwargs):

        books = self.model.objects.get(id=kwargs.get("id"))
        feedbacks = self.feedback_model.objects.filter(book_id=books)
        context = {"feedbacks": feedbacks, "id": kwargs.get("id")}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        books = self.model.objects.get(id=kwargs.get("id"))
        feedbacks = self.feedback_model.objects.filter(book_id=books)
        form = self.form_class(request.POST or None, instance=feedbacks.first())
        if form.is_valid():
            form.save()
            messages.success(request, "The post has been updated successfully.")
            return redirect(self.success_url)
        else:
            messages.error(request, "Please correct the following errors:")
            return render(request, self.template_name, {"form": form})
