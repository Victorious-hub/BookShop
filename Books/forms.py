from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm

from Books.models import Book, Feedback
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'desc': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['book_name'].widget.attrs['class'] = 'form-control'
        self.fields['book_author'].widget.attrs['class'] = 'form-control'
        self.fields['desc'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['book_image'].widget.attrs['class'] = 'form-control'
        self.fields['genre'].widget.attrs['class'] = 'form-control'


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('header','description')
        widgets = {
            'desc': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['header'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'


