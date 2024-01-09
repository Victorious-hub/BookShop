from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from BookShop import settings
from book.views import (
    Main,
    CreateBookView,
    AddToWishlistView,
    BookUpdateView,
    BookDeleteView,
    RemoveWishList,
    SearchBooksView,
    CartView,
    AddToCartView,
    AuthenticatedView,
    RemoveAllCartView,
    AddFeedBackView,
    CheckersView,
    CreatePDFView,
    BookDetailView,
    AcceptContact,
    EditFeedbackView,
    DeleteFeedBackView,
    RemoveFromCart
)
from users.views import (
    SignOut,
    EditProfileView,
    AddHyperlinksView,
    SignIn,
    SignUpView,
    ChangePasswordView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', SignUpView.as_view(), name='register'),
    path('', Main.as_view(), name='main'),
    path('login/', SignIn.as_view(), name='login'),
    path('logout/', SignOut.as_view(), name='logout'),
    path('add_book/', CreateBookView.as_view(), name='add_book'),
    path('add_to_wishlist', AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('book_edit/<int:id>', BookUpdateView.as_view(), name='book_edit'),
    path('book_delete/<int:pk>', BookDeleteView.as_view(), name='book_delete'),
    path('remove_wishlist', RemoveWishList.as_view(), name='remove_wishlist'),
    path('search_books', SearchBooksView.as_view(), name='book_search'),
    path('profile_edit/<slug:slug>', EditProfileView.as_view(), name='edit_profile'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add_to_cart', AddToCartView.as_view(), name='add'),
    path('authenticated/', AuthenticatedView.as_view(), name='tovar_page'),
    path('remove_from_cart', RemoveFromCart.as_view(), name='remove_from_cart'),
    path('remove_all', RemoveAllCartView.as_view(), name='remove_all_cart'),
    path('add_feedback/<int:id>', AddFeedBackView.as_view(), name='add_feedback'),
    path('checkers', CheckersView.as_view(), name='checkers'),
    path('change_password/<int:id>', ChangePasswordView.as_view(), name='change_password'),
    path('add_hyperlinks/<int:id>', AddHyperlinksView.as_view(), name='add_hyperlinks'),
    path('create_pdf/<int:id>', CreatePDFView.as_view(), name='create_pdf'),
    path('book_detail/<int:id>', BookDetailView.as_view(), name='book_detail'),
    path('contact_us', AcceptContact.as_view(), name='accept_contact'),
    path('delete_feedback/<int:id>', DeleteFeedBackView.as_view(), name='delete_feedback'),
    path('edit_feedback/<int:id>', EditFeedbackView.as_view(), name='edit_feedback'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
