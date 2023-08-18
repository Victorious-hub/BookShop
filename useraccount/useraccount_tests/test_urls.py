from unittest import TestCase

from django.test import SimpleTestCase
from django.urls import reverse, resolve
import random

from useraccount.forms import EditForm
from useraccount.views import EditProfileView, SignOut, SignIn, SignUpView, AddHyperlinksView


class TestUrls(SimpleTestCase):

    def test_edit_profile(self):
        url = reverse('edit_profile', args=['slug'])
        self.assertEquals(resolve(url).func.view_class, EditProfileView)

    def test_logout(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, SignOut)

    def test_login(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, SignIn)

    def test_register(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class, SignUpView)

    def test_hyperlinks(self):
        id_value = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        url = reverse('add_hyperlinks', args=[random.choice(id_value)])
        self.assertEquals(resolve(url).func.view_class, AddHyperlinksView)
