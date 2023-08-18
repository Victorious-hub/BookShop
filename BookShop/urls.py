from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from Books import views
from rest_framework import permissions
from Books.views import *
from useraccount.views import (
    SignOut,
    EditProfileView,
    AddHyperlinksView,
    SignIn,
    SignUpView
)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
                  path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                       name='schema-json'),
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                  path('admin/', admin.site.urls),
                  path('register/', SignUpView.as_view(), name='register'),

                  path('main/', Main.as_view(), name='main'),

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

                  path('authenticated/', AuthenticatedView.as_view(), name='authenticated'),

                  path('remove_from_cart', RemoveFromCartView.as_view(), name='remove_from_cart'),

                  path('remove_all', RemoveAllCartView.as_view(), name='remove_all_cart'),

                  path('add_feedback/<int:id>', AddFeedBackView.as_view(), name='add_feedback'),

                  path('feedbacks/<int:id>', FeedBacksView.as_view(), name='feedbacks'),

                  path('checkers', CheckersView.as_view(), name='checkers'),

                  path('price_checkers', PriceCheckersView.as_view(), name='price_checkers'),

                  path('change_password/<int:id>', ChangePasswordView.as_view(), name='change_password'),

                  path('add_hyperlinks/<int:id>', AddHyperlinksView.as_view(), name='add_hyperlinks'),

                  path('create_pdf/<int:id>', CreatePDFView.as_view(), name='create_pdf'),

                  path('book_detail/<int:id>', BookDetailView.as_view(), name='book_detail'),

                  path('contact_us', AcceptContact.as_view(), name='accept_contact'),

                  path('delete_feedback/<int:id>', DeleteFeedBackView.as_view(), name='delete_feedback'),

                  path('edit_feedback/<int:id>',EditFeedbackView.as_view(), name='edit_feedback'),

                  path('test',AcceptedOrders.as_view(),name='lox'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
