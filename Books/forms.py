from django import forms
from Books.models import Book, Feedback, Contact


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
        self.fields['book_year'].widget.attrs['class'] = 'form-control'
        self.fields['book_author'].widget.attrs['class'] = 'form-control'
        self.fields['desc'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['book_image'].widget.attrs['class'] = 'form-control'
        self.fields['genre'].widget.attrs['class'] = 'form-control'


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('header', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['header'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name', 'address', 'email', 'phone')

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['class'] = 'form-control'
