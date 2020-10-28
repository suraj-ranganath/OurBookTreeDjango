from django.shortcuts import render
from .forms import *
# Create your views here.


def BookGiveFormView(request):
    book_form = BookForm(request.POST or None)
    if book_form.is_valid():
        book_form.save()
        book_form = BookForm()
    
    give_form = GiveForm(request.POST or None)
    if give_form.is_valid():
        give_form.save()
        give_form = GiveForm()

    give_order_form = GiveOrderForm(request.POST or None)
    if give_order_form.is_valid():
        give_order_form.save()
        give_order_form = GiveOrderForm()

    context ={
        'book_form':book_form,
        'give_form':give_form,
        'give_order_form':give_order_form,
    }
    return render(request,"giveform.html",context)