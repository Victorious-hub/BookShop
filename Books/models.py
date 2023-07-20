import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

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
class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email or len(email) <= 0:
            raise ValueError("Email field is required !")
        if not password:
            raise ValueError("Password is must !")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser):
    first_name = models.CharField(default="", max_length=255)

    email = models.EmailField(default="", max_length=200, unique=True)

    last_name = models.CharField(default="", max_length=255)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = "email"

    objects = UserAccountManager()

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class SimpleUser(UserAccount):
    created = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return 'Пользователь {}'.format(self.first_name)





class Feedback(models.Model):
    author = models.ForeignKey(SimpleUser, on_delete=models.CASCADE)
    header = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=255, default='')
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)

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
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(SimpleUser, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def total_price(self):
        wisthlistitems = self.wisthlistitems.all()
        total = sum([item.price for item in wisthlistitems])
        return total

    @property
    def num_of_items(self):
        wisthlistitems = self.wisthlistitems.all()
        quantity = sum([item.quantity for item in wisthlistitems])
        return quantity


class WisthlistItem(models.Model):
    book_product = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="witems")
    wisthlist_item = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="wisthlistitems")
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.book_product.book_name

    @property
    def price(self):
        new_price = self.book_product.price * self.quantity
        return new_price
