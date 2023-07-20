from django.contrib import admin
from .models import *
admin.site.register(Book)
admin.site.register(SimpleUser)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(WishList)
admin.site.register(WisthlistItem)
admin.site.register(Feedback)