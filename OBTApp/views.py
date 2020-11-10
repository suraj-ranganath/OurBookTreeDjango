from django.shortcuts import render
from .forms import *
from .models import *
from django.db import connection
# Create your views here.
cursor = connection.cursor()

def BookGiveFormView(request):
    if request.method == 'POST':
        book_form = BookForm(request.POST or None)
        give_order_form = GiveOrderForm(request.POST or None)   

        #give_form = GiveForm(request.POST or None,initial={'email':request.user.email})
        '''
        if give_order_form.is_valid() and book_form.is_valid():
            book = book_form.save()
            give_order = give_order_form.save(False)    

            give = Give(email=request.user.email)
            give.save()
            #give = give_form.save()

            give_order.bookID = book
            give_order.save()
            give_order.giveNo = give 
            book_form = BookForm()
            give_order_form = GiveOrderForm()
        '''   
        context ={
            'book_form':book_form,
            'give_order_form':give_order_form,
            'email':request.user.email,
        }
        return render(request,"giveform.html",context)
    else:
        book_form = BookForm(request.POST or None)
        give_order_form = GiveOrderForm(request.POST or None) 
        #give_form = GiveForm(request.GET or None, initial = {'email':request.user.email})

        context ={
            'book_form':book_form,
            'give_order_form':give_order_form,
            #'give_form':give_form,
            'email':request.user.email,
        }
        return render(request,"giveform.html",context)
