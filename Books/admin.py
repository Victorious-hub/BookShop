from django.contrib import admin
from .models import Book, Cart, CartItem, WishList, WisthlistItem, Feedback, Contact
admin.site.register(Book)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(WishList)
admin.site.register(WisthlistItem)
admin.site.register(Feedback)
admin.site.register(Contact)