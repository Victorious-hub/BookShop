from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Books.views import (

    CreateBookView,
    AddToWishlistView,
    BookUpdateView,
    BookDeleteView,
    RemoveWishList,
    CartView,
    AddToCartView,
    AuthenticatedView,
    RemoveFromCart,
    RemoveAllCartView,
    AddFeedBackView,
    CreatePDFView,
    AcceptContact,
    DeleteFeedBackView,
    EditFeedbackView,

)
from useraccount.views import ChangePasswordView


class TestUrls(SimpleTestCase):
    def test_add_book(self):
        url = reverse('add_book')
        self.assertEquals(resolve(url).func.view_class, CreateBookView)

    def test_add_to_wishlist(self):
        url = reverse('add_to_wishlist')
        self.assertEquals(resolve(url).func.view_class, AddToWishlistView)

    def test_book_edit(self):
        url = reverse('book_edit', args=[1])
        self.assertEquals(resolve(url).func.view_class, BookUpdateView)

    def test_book_delete(self):
        url = reverse('book_delete', args=[1])
        self.assertEquals(resolve(url).func.view_class, BookDeleteView)

    def test_remove_wishlist(self):
        url = reverse('remove_wishlist')
        self.assertEquals(resolve(url).func.view_class, RemoveWishList)

    def test_cart(self):
        url = reverse('cart')
        self.assertEquals(resolve(url).func.view_class, CartView)

    def test_add_to_cart(self):
        url = reverse('add')
        self.assertEquals(resolve(url).func.view_class, AddToCartView)

    def test_authenticated(self):
        url = reverse('tovar_page')
        self.assertEquals(resolve(url).func.view_class, AuthenticatedView)

    def test_remove_from_cart(self):
        url = reverse('remove_from_cart')
        self.assertEquals(resolve(url).func.view_class, RemoveFromCart)

    def test_remove_all_cart(self):
        url = reverse('remove_all_cart')
        self.assertEquals(resolve(url).func.view_class, RemoveAllCartView)

    def test_add_feedback(self):
        url = reverse('add_feedback', args=[1])
        self.assertEquals(resolve(url).func.view_class, AddFeedBackView)

    def test_change_password(self):
        url = reverse('change_password', args=[1])
        self.assertEquals(resolve(url).func.view_class, ChangePasswordView)

    def test_create_pdf(self):
        url = reverse('create_pdf', args=[1])
        self.assertEquals(resolve(url).func.view_class, CreatePDFView)

    def test_accept_contact(self):
        url = reverse('accept_contact')
        self.assertEquals(resolve(url).func.view_class, AcceptContact)

    def test_delete_feedback(self):
        url = reverse('delete_feedback', args=[1])
        self.assertEquals(resolve(url).func.view_class, DeleteFeedBackView)

    def test_edit_feedback(self):
        url = reverse('edit_feedback',args=[1])
        self.assertEquals(resolve(url).func.view_class, EditFeedbackView)
