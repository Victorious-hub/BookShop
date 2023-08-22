import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail, BadHeaderError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, DeleteView, ListView, UpdateView, CreateView, DetailView
from rest_framework.permissions import IsAdminUser
from django.db.models import Q
from useraccount.models import SimpleUser
from .models import Book, CartItem, Cart, Feedback, WishList, WisthlistItem, Contact
from .forms import BookForm, FeedbackForm, ContactForm
from django.contrib import messages
from django.core.paginator import Paginator
from .tasks import sleeptime
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.conf import settings


class CreatePDFView(LoginRequiredMixin, View):
    def get(self, request, id):
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
    def get(self, request):
        cart = None
        cartitems = []
        if request.user.is_authenticated and not request.user.is_admin:
            cart, created = Cart.objects.get_or_create(user=request.user.simpleuser, completed=False)
            cartitems = cart.cartitems.all()
        context = {"cart": cart, "items": cartitems}
        return render(request, 'Cart/CartTest.html', context)


class AddToCartView(View):
    def post(self, request):
        data = json.loads(request.body)
        print(data)
        product_id = data["id"]
        product = Book.objects.get(id=product_id)

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user.simpleuser, completed=False)

            cartitem, created = CartItem.objects.get_or_create(cart=cart, book_product=product)

            cartitem.quantity += 1

            cartitem.save()

            num_of_item = cart.num_of_items

        return JsonResponse("Working", safe=False)


class RemoveFromCartView(View):
    def post(self, request):
        data = json.loads(request.body)
        product_id = data["id"]
        product = Book.objects.get(id=product_id)

        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user.simpleuser, completed=False)

            cartitem = CartItem.objects.get(cart=cart, book_product=product)

            if cartitem.quantity >= 1:
                cartitem.quantity -= 1
                cartitem.save()
            else:
                cartitem.delete()

            num_of_item = cart.num_of_items

            print(cartitem)
        return JsonResponse({'price': cartitem.price, 'num_of_items': num_of_item}, safe=False)


class RemoveAllCartView(LoginRequiredMixin, View):
    def post(self, request, id):
        data = json.loads(request.body)
        product_id = data["id"]
        product = Book.objects.get(id=product_id)

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user.simpleuser, completed=False)

            cartitem, created = CartItem.objects.get_or_create(cart=cart, book_product=product)

            cartitem.delete()

            num_of_item = cart.num_of_items

        return JsonResponse({'price': cartitem.price, 'num_of_items': num_of_item}, safe=False)


class Main(TemplateView):
    template_name = 'users/main.html'


class ChangePasswordView(LoginRequiredMixin, View):
    def post(self, request, id):
        profile = SimpleUser.objects.get(id=id)
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('register')
        else:
            messages.error(request, 'Please correct the error below.')
        return render(request, 'users/profile_change.html', {'form': form})


class BookDetailView(LoginRequiredMixin, DetailView):
    model = [Book, Feedback]
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get(self, request, id):
        book = self.model[0].objects.get(id=id)
        feedbacks = self.model[1].objects.filter(book_id=book)
        context = {'book': book, 'feedbacks': feedbacks}
        return render(request, self.template_name, context)


class AuthenticatedView(LoginRequiredMixin, TemplateView):
    template_name = 'users/authenticated.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()

        p = Paginator(Book.objects.all(), 2)
        page = self.request.GET.get('page')

        books_page = p.get_page(page)

        context['books_page'] = books_page
        context['nums'] = "a" * books_page.paginator.num_pages
        if self.request.user.is_authenticated and not self.request.user.is_admin:
            cart, created = Cart.objects.get_or_create(user=self.request.user.simpleuser, completed=False)
        return context


def test(request):
    contact = Contact.objects.all()
    print(contact)
    return render(request, 'books/test.html', {"contact": contact})


@method_decorator(login_required, name="dispatch")
class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('main')
    template_name = 'books/delete_book.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())
        else:
            raise Http404


class SearchBooksView(LoginRequiredMixin, View):
    def post(self, request):
        searched = request.POST['searched']
        if (len(searched) != 0):
            book_names = Book.objects.filter(Q(book_name__contains=searched) | Q(book_author__contains=searched))
            return render(request, 'books/search_book.html', {'searched': searched, 'book_names': book_names, })
        else:
            return render(request, 'books/search_book.html', {})


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/edit-book.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CreateBookView(LoginRequiredMixin, CreateView):
    form_class = BookForm
    template_name = 'books/add_book.html'
    success_url = reverse_lazy('authenticated')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AddFeedBackView(LoginRequiredMixin, View):
    model = [Book, Feedback]
    template_name = 'Feedback/add_feedback.html'
    form_class = FeedbackForm

    def get(self, request, id):
        books = self.model[0].objects.get(id=id)
        feedbacks = self.model[1].objects.filter(book_id=books)
        context = {'form': self.form_class(instance=books), 'id': id}
        return render(request, self.template_name, context)

    def post(self, request, id):
        books = self.model[0].objects.get(id=id)
        feedbacks = self.model[1].objects.filter(book_id=books)
        if len(feedbacks) == 0:
            form = self.form_class(request.POST)
            if form.is_valid():
                feedback = form.save(commit=False)
                feedback.author = request.user.simpleuser
                feedback.book_id = books
                feedback.save()
                return redirect('authenticated')

            else:
                messages.error(request, 'Please correct the following errors:')
                return render(request, self.template_name, {'form': form})
        return render(request, 'users/authenticated.html', )


class FeedBacksView(LoginRequiredMixin, View):
    def get(self, request, id):
        books = Book.objects.get(id=id)
        feedbacks = Feedback.objects.filter(book_id=books)
        context = {'feedbacks': feedbacks}
        return render(request, 'Feedback/feedbacks.html', context)


class CheckersView(LoginRequiredMixin, View):
    def post(self, request):
        searched = request.POST.getlist('searched')
        books = Book.objects.filter(genre__in=searched)
        context = {'books': books}
        return render(request, 'books/checker.html', context)


# return render(request, 'books/checker.html', )


class PriceCheckersView(LoginRequiredMixin, View):
    def post(self, request):
        price_min = request.POST.get('priceMin')
        price_max = request.POST.get('priceMax')
        books = Book.objects.filter(price__gte=price_min, price__lte=price_max)
        context = {'books': books}
        return render(request, 'books/price_checker.html', context)

    # return render(request, 'books/price_checker.html')


class AddToWishlistView(View):
    def post(self, request):
        data = json.loads(request.body)
        product_id = data["id"]
        product = Book.objects.get(id=product_id)

        if request.user.is_authenticated:
            cart, created = WishList.objects.get_or_create(user=request.user.simpleuser, completed=False)
            cart.save()
            cartitem, created = WisthlistItem.objects.get_or_create(wisthlist_item=cart, book_product=product)

            cartitem.quantity += 1
            cartitem.save()
        return JsonResponse("Working", safe=False)


class RemoveWishList(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        product_id = data["id"]
        product = Book.objects.get(id=product_id)

        if request.user.is_authenticated:
            cart, created = WishList.objects.get_or_create(user=request.user.simpleuser, completed=False)
            cart.save()

            cartitem, created = WisthlistItem.objects.get_or_create(wisthlist_item=cart, book_product=product)

            cartitem.quantity -= 1
            cartitem.remove()
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
    model = [Book, Feedback]
    success_url = reverse_lazy('main')
    template_name = 'users/profile_change.html'

    def get(self, request, id):
        books = self.model[0].objects.get(id=id)
        feedbacks = self.model[1].objects.filter(book_id=books).delete()

        messages.success(request, 'The post has been deleted successfully.')
        return redirect(self.success_url)


class EditFeedbackView(LoginRequiredMixin, View):
    model = [Book, Feedback]
    template_name = 'users/profile_change.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('main')

    def get(self, request, id):
        books = self.model[0].objects.get(id=id)
        feedbacks = self.model[1].objects.filter(book_id=books)
        context = {'feedbacks': feedbacks, 'id': id}
        return render(request, self.template_name, context)

    def post(self, request, id):
        books = self.model[0].objects.get(id=id)
        feedbacks = self.model[1].objects.filter(book_id=books)
        form = FeedbackForm(request.POST or None, instance=feedbacks.first())
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been updated successfully.')
            return redirect(self.success_url)
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request, self.template_name, {'form': form})
