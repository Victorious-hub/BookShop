from django.contrib import admin

from Books.models import Book,SimpleUser
admin.site.register(Book)
admin.site.register(SimpleUser)

