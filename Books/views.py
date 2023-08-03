import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAdminUser
from django.db.models import Q
from useraccount.forms import HyperLinkkForm
from useraccount.models import SimpleUser
from .models import Book, CartItem, Cart, Feedback, WishList, WisthlistItem
from .forms import BookForm, FeedbackForm
from django.contrib import messages
from django.core.paginator import Paginator
from .tasks import sleeptime
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_pdf(request, id):
    # book_id = request.POST.get('book_id')
    book = Book.objects.get(id=id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="BookReview.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)

    title_font_size = 16
    content_font_size = 12
    page_width, page_height = letter

    title = book.book_name

    # Add page 1
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


def payment(request):
    return render(request, 'Payment/PayPal.html', {})


def cart(request):
    cart = None
    cartitems = []
    if request.user.is_authenticated and not request.user.is_admin:
        cart, created = Cart.objects.get_or_create(user=request.user.simpleuser, completed=False)
        cartitems = cart.cartitems.all()
    context = {"cart": cart, "items": cartitems}
    return render(request, 'Cart/CartTest.html', context)


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
    return render(request, 'users/base.html', {})


@login_required
def change_password(request, id):
    profile = SimpleUser.objects.get(id=id)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('register')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/profile_change.html', {
        'form': form
    })


@login_required
def authenticated(request):
    books = Book.objects.all()

    p = Paginator(Book.objects.all(), 2)
    page = request.GET.get('page')
    books_page = p.get_page(page)

    nums = "a" * books_page.paginator.num_pages

    if request.user.is_authenticated and not request.user.is_admin:
        cart, created = Cart.objects.get_or_create(user=request.user.simpleuser, completed=False)
    context = {'books': books, 'books_page': books_page, "nums": nums, }
    return render(request, 'users/authenticated.html', context)


"""class ProfileListView(generics.ListCreateAPIView):
    queryset = models.SimpleUser.objects.all()
    serializer_class = serializer.UserSerializer


class ProfileChange(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SimpleUser.objects.all()
    serializer_class = serializer.UserSerializer"""


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


@login_required
def checkers(request):
    if request.method == 'POST':
        searched = request.POST.getlist('searched')
        books = Book.objects.filter(genre__in=searched)
        context = {'books': books}
        return render(request, 'books/checker.html', context)

    return render(request, 'books/checker.html', )


@login_required
def price_checkers(request):
    if request.method == 'POST':
        price_min = request.POST.get('priceMin')
        price_max = request.POST.get('priceMax')
        books = Book.objects.filter(price__gte=price_min, price__lte=price_max)
        context = {'books': books}
        return render(request, 'books/price_checker.html', context)

    return render(request, 'books/price_checker.html')


def add_to_wishlist(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = Book.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart, created = WishList.objects.get_or_create(user=request.user.simpleuser, completed=False)
        cart.save()  # Сохраняем объект cart

        cartitem, created = WisthlistItem.objects.get_or_create(wisthlist_item=cart, book_product=product)

        cartitem.quantity += 1
        cartitem.save()
    return JsonResponse("Working", safe=False)


def remove_from_wishlist(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = Book.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart, created = WishList.objects.get_or_create(user=request.user.simpleuser, completed=False)
        cart.save()  # Сохраняем объект cart

        cartitem, created = WisthlistItem.objects.get_or_create(wisthlist_item=cart, book_product=product)

        cartitem.quantity -= 1
        cartitem.remove()
    return JsonResponse("Working", safe=False)


def wishlist(request):
    cart = None
    cartitems = []
    if request.user.is_authenticated and not request.user.is_admin:
        cart, created = WishList.objects.get_or_create(user=request.user.simpleuser, completed=False)
        cartitems = cart.wisthlistitems.all()
    context = {"cart": cart, "items": cartitems}
    return render(request, 'Feedback/Wishlist.html', context)
