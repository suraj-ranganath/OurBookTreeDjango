from django import forms
from .models import Book,Give,GiveOrder

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['grade','bookName','subject']

class GiveOrderForm(forms.ModelForm):
    class Meta:
        model = GiveOrder
        fields = ['quantity','yearPub','condition']