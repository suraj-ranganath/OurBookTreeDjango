from django.shortcuts import render
from .forms import *
from .models import *
# Create your views here.


def BookGiveFormView(request):
    if request.method == 'POST':
        book_form = BookForm(request.POST or None)
        give_order_form = GiveOrderForm(request.POST or None)   

        '''
        initial_data = {'email':'a@b.com'}
        obj = Give.objects.get(id=1)
        give_form = GiveForm(request.POST or None,instance=obj)
        if give_form.is_valid():
            give_form.save()
            give_form = GiveForm()
        '''
        if give_order_form.is_valid() and book_form.is_valid():
            book = book_form.save()
            give_order = give_order_form.save(False)    
            
            give_order.bookID = book
            give_order.save()
            book_form = BookForm()
            give_order_form = GiveOrderForm()   
        context ={
            'book_form':book_form,
            'give_order_form':give_order_form,
            #'give_form':give_form,
        }
        return render(request,"giveform.html",context)
    else:
        book_form = BookForm(request.POST or None)
        give_order_form = GiveOrderForm(request.POST or None) 
        context ={
            'book_form':book_form,
            'give_order_form':give_order_form,
            #'give_form':give_form,
        }
        return render(request,"giveform.html",context)
