from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import SimpleUser, HyperLinks


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


class HyperLinkkForm(forms.ModelForm):
    class Meta:
        model = HyperLinks
        fields = ('user_linkedin', 'user_github')

    def __init__(self, *args, **kwargs):
        super(HyperLinkkForm, self).__init__(*args, **kwargs)
        self.fields['user_linkedin'].widget.attrs['class'] = 'form-control'
        self.fields['user_github'].widget.attrs['class'] = 'form-control'
