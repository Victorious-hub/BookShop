from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


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


class HyperLinks(models.Model):
    user_linkedin = models.URLField(max_length=200)
    user_github = models.URLField(max_length=200)
    user = models.ForeignKey(SimpleUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
