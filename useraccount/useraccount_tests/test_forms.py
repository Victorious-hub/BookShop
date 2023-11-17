from unittest import TestCase

from accounts.forms import (
    EditForm,
    LoginForm,
    HyperLinkkForm,
    RegisterForm
)


class TestForms(TestCase):  # ?

    def test_edit_form(self):
        form = EditForm(data={
            'first_name': 'Victor',
            'last_name': 'Shyshko',
            'email': 'vitya@gmail.com'
        })
        self.assertTrue(form.is_valid())

    def test_edit_form_no_data(self):
        form = EditForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_login_form(self):
        form = LoginForm(data={
            'email': 'vitya@gmail.com',
            'password': '63254890Bb'
        })
        self.assertTrue(form.is_valid())

    def test_login_form_no_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_hyperlink_form(self):
        form = HyperLinkkForm(data={
            'user_linkedin': 'https://education.github.com/globalcampus/exchange',
            'user_github': 'https://education.github.com/globalcampus/exchange'
        })
        self.assertTrue(form.is_valid())

    def test_hyperlink_form_no_data(self):
        form = HyperLinkkForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_register_form(self):
        form = RegisterForm(data={
            'first_name': 'Victor',
            'last_name': 'Shyshko',
            'email': 'shyshkov745@gmail.com',
            'password1': '63254890Ba'
        })
        self.assertTrue(form.is_valid())

    def test_register_form_no_data(self):
        form = RegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)
