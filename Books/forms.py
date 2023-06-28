from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm

from Books.models import SimpleUser, Book


class RegisterForm(UserCreationForm):
    class Meta:
        model = SimpleUser
        fields = ['first_name', 'last_name', 'email']

    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', })),
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'})),
    email = forms.CharField(max_length=255, widget=forms.EmailInput(attrs={'class': 'form-control'})),
    password1 = forms.CharField(max_length=255, widget=forms.EmailInput(attrs={'class': 'form-control'})),

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        del self.fields['password2']
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'


class EditForm(forms.ModelForm):
    class Meta:
        model = SimpleUser
        fields = ['first_name', 'last_name', 'email']

    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', })),
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'})),
    email = forms.CharField(max_length=255, widget=forms.EmailInput(attrs={'class': 'form-control'})),

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'


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


class LoginForm(forms.Form):
    class Meta:
        model = SimpleUser
        fields = ['email', 'password']

    email = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
