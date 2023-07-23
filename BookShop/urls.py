from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

import useraccount
from Books import views

from rest_framework import permissions
from Books.views import *
from useraccount.views import (sign_in,
                               sign_up,sign_out,edit_profile
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
    path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('register/', sign_up.as_view(), name='register'),

   # path('api/profilelist/', Books.views.ProfileListView.as_view(),
                       #name="name"),

   # path('api/profilelist/<int:pk>', Books.views.ProfileChange.as_view(),
                      # name="name"),

    path('main/', views.main, name='main'),

    path('login/', useraccount.views.sign_in, name='login'),

    path('logout/', useraccount.views.sign_out, name='logout'),

    path('add_book/', views.add_book, name='add_book'),
    path('add_to_wishlist', views.add_to_wishlist, name='add_to_wishlist'),

    path('book_edit/<int:id>', views.edit_book, name='book_edit'),
    path('book_delete/<int:id>', views.delete_book, name='book_delete'),

    path('book_delete/<int:id>', views.delete_book, name='book_delete'),

    path('wishlist', views.wishlist, name='wishlist'),

    path('remove_wishlist', views.remove_from_wishlist, name='remove_wishlist'),

    path('search_books',views.search_books,name='book_search'),

    path('profile_edit/<int:id>', useraccount.views.edit_profile, name='edit_profile'),

    path('cart/', views.cart, name='cart'),

    path('add_to_cart', views.add_to_cart, name='add'),

    path('authenticated/', views.authenticated, name='authenticated'),

    path('remove_from_cart', views.remove_from_cart, name='add_wishlist'),

    path('remove_all', views.remove_all, name='remove_all_cart'),

    path('add_feedback/<int:id>', views.add_feedback, name='add_feedback'),

    path('feedbacks/<int:id>', views.feedbacks, name='feedbacks'),

    path('checkers', views.checkers, name='checkers'),

    path('price_checkers', views.price_checkers, name='price_checkers'),

    path('pay_paypal',views.payment,name='pay_paypal')

]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
