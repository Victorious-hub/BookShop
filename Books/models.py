import uuid

from django.db import models
from django.utils import timezone

from useraccount.models import SimpleUser

tz = timezone.get_default_timezone()


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    GENRE = (
        ('Fantasy', 'Fantasy'),
        ('Adventure', 'Adventure'),
        ('Love', 'Love'),
        ('Historic', 'Historic'),
        ('Detective', 'Detective'),
    )

    book_name = models.CharField(max_length=255, null=False)
    book_author = models.CharField(max_length=255, null=False)
    desc = models.TextField()
    genre = models.CharField(max_length=255, null=True, choices=GENRE)
    price = models.IntegerField(max_length=100, default=0)
    book_image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return str(self.id)


class Feedback(models.Model):
    author = models.ForeignKey(SimpleUser, on_delete=models.CASCADE)
    header = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=255, default='')
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_released = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return str(self.author)


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(SimpleUser, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def total_price(self):
        cartitems = self.cartitems.all()
        total = sum([item.price for item in cartitems])
        return total

    @property
    def num_of_items(self):
        cartitems = self.cartitems.all()
        quantity = sum([item.quantity for item in cartitems])
        return quantity


class CartItem(models.Model):
    book_product = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="items")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartitems")
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.book_product.book_name

    @property
    def price(self):
        new_price = self.book_product.price * self.quantity
        return new_price


class WishList(models.Model):
    user = models.ForeignKey(SimpleUser, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class WisthlistItem(models.Model):
    book_product = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="witems")
    wisthlist_item = models.ForeignKey(WishList, on_delete=models.CASCADE, related_name="wisthlistitems")
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.book_product.book_name


