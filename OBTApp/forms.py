from django import forms
from .models import Book,Give,GiveOrder

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['grade','bookName','subject']


class GiveForm(forms.ModelForm):
    class Meta:
        model = Give
        fields = ['email']

class GiveOrderForm(forms.ModelForm):
    class Meta:
        model = GiveOrder
        fields = ['quantity','yearPub','condition']