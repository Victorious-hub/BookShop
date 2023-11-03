from unittest import TestCase
from Books.forms import (
    FeedbackForm,
    ContactForm,
    BookForm
)


class TestForms(TestCase):  # ?

    def test_feedback_form(self):
        form = FeedbackForm(data={
            'header': 'How to become a programmer',
            'description': 'Lorem Ipsum',
        })
        self.assertTrue(form.is_valid())

    def test_edit_form_no_data(self):
        form = FeedbackForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_contact_form(self):
        form = ContactForm(data={
            'first_name': 'Victor',
            'address': 'Krupitsa street',
            'email': 'vitya@lox.com',
            'phone': '+1234512345'
        })
        self.assertTrue(form.is_valid())

    def test_contact_no_data(self):
        form = ContactForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)
