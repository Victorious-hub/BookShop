from django.http import response
from django.test import TestCase, Client
from django.urls import reverse

from Books.models import Cart
from useraccount.models import *
import json


class TestViews(TestCase):
    client = Client()
    simpleuser, created = SimpleUser.objects.get_or_create(
        first_name='John',
        last_name='Doe',
        email='john@example.com',
        password='12345',
    )

    hyper_user, created = HyperLinks.objects.get_or_create(
        user=simpleuser,
        user_linkedin='https://www.youtube.com/watch?v=hA_VxnxCHbo',
        user_github='https://www.youtube.com/watch?v=hA_VxnxCHbo',
    )

    cart, created = Cart.objects.get_or_create(
        id=1,
        user=simpleuser,
        completed=False
    )

    def test_sign_in_GET(self):
        response_reverse = self.client.get(reverse('login'))

        self.assertEquals(response_reverse.status_code, 200)

        self.assertTemplateUsed(response_reverse, 'users/login.html')

    def test_sign_up_GET(self):
        response_reverse = self.client.get(reverse('register'))

        self.assertEquals(response_reverse.status_code, 200)

        self.assertTemplateUsed(response_reverse, 'users/register.html')

    def test_sign_up_POST(self):
        response_reverse = self.client.post(reverse('register'), {
            'first_name': self.simpleuser.first_name,
            'last_name': self.simpleuser.last_name,
            'email': self.simpleuser.email,
            'password': self.simpleuser.password,
        })
        self.assertEquals(response_reverse.status_code, 200)
        self.assertTemplateUsed(response_reverse, 'users/register.html')

    def test_hyperlinks_POST(self):
        response_reverse = self.client.post(reverse('add_hyperlinks', args=[1]), {
            'user_linkedin': self.hyper_user.user_linkedin,
            'user_github': self.hyper_user.user_github,
            'user': self.simpleuser
        })

        self.assertEquals(response_reverse.status_code, 302)
        #self.assertTemplateUsed(response_reverse, 'users/main.html')

    def test_logout_GET(self):
        response_reverse = self.client.get(reverse('logout'))
        self.assertEquals(response_reverse.status_code,302)

        self.assertEquals(self.client.get(reverse('register')).status_code, 200)

    def test_profile_change_orders(self):
        response_reverse = self.client.get(reverse('edit_profile',args=['slug']))
        self.assertEquals(response_reverse.status_code,302)



