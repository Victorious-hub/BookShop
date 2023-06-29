from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import Books
from Books import views
from Books.views import sign_up, sign_out, sign_in

from django.conf import settings
from django.conf.urls.static import static

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

    path('api/profilelist/', Books.views.ProfileListView.as_view(),
                       name="name"),

    path('api/profilelist/<int:pk>', Books.views.ProfileChange.as_view(),
                       name="name"),

    path('main/', views.main, name='main'),

    path('login/', sign_in.as_view(), name='login'),

    path('logout/', views.sign_out, name='logout'),

    path('add_book/', views.add_book, name='add_book'),

    path('book_edit/<int:id>', views.edit_book, name='book_edit'),
    path('book_delete/<int:id>', views.delete_book, name='book_delete'),

    path('book_delete/<int:id>', views.delete_book, name='book_delete'),

    path('search_books',views.search_books,name='book_search'),

    path('profile_edit/<int:id>', views.edit_profile, name='edit_profile'),

    path('cart/', views.cart, name='cart'),

    path('add_to_cart', views.add_to_cart, name='add'),

    path("confirm_payment/<str:pk>", views.confirm_payment, name="add"),



]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
