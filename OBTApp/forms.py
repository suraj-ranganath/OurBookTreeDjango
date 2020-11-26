from django import forms
from .models import Book,Give,GiveOrder
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
'''
class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phoneNo=forms.CharField(max_length=10, required=False, help_text='Optional.')
    location=forms.CharField(max_length=1000, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'phoneNo', 'location', 'password1', 'password2', )
'''
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    phoneNo=forms.CharField(max_length=10, required=False, help_text='Optional.')
    location=forms.CharField(max_length=1000, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'phoneNo', 'location', 'password1', 'password2', )

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['grade','bookName','subject']
'''
class GiveForm(forms.ModelForm):
    class Meta:
        model = Give
        fields = ['email']
        email = forms.CharField()
'''

class GiveOrderForm(forms.ModelForm):
    class Meta:
        model = GiveOrder
        fields = ['quantity','yearPub','condition']