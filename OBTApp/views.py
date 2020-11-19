from django.shortcuts import render
from .forms import *
from .models import *
from django.db import connection
# Create your views here.
cursor = connection.cursor()

def BookGiveFormView(request):
    if request.method == 'POST':

        email=request.user.email
        grade=request.POST["grade"]
        bookname=request.POST["bookname"]
        subject=request.POST["subject"]
        quan=request.POST["quan"]
        yearpub=request.POST["yearpub"]
        condition=request.POST["condition"]

        cursor.execute("insert into obtapp_book (grade,bookName,subject) values ('{}','{}','{}')".format(grade,bookname,subject))
        cursor.execute("insert into obtapp_give (email_id,completedFlag) values ('{}',0)".format(email))
        cursor.execute("select id from obtapp_book where id=(select max(id) from obtapp_book)")
        bookid=cursor.fetchall()[0][0]
        cursor.execute("select id from obtapp_give where id=(select max(id) from obtapp_give)")
        giveno=cursor.fetchall()[0][0]
        cursor.execute("insert into obtapp_giveorder (quantity,yearPub,`condition`,completedFlag,bookID_id,giveNo_id) values ({},'{}','{}',0,{},{})".format(quan,yearpub,condition,bookid,giveno))
        # book_form = BookForm()
        # give_order_form = GiveOrderForm()   

        # give_form = GiveForm(request.POST or None,initial={'email':request.user.email})
        
        # if give_order_form.is_valid() and book_form.is_valid():
        #     book = book_form.save()
        #     give_order = give_order_form.save(False)    

        #     give = Give(email=request.user.email)
        #     give.save()
        #     give = give_form.save()

        #     give_order.bookID = book
        #     give_order.save()
        #     give_order.giveNo = give 
        #     book_form = BookForm()
        #     give_order_form = GiveOrderForm()
          
        context ={
            # 'book_form':book_form,
            # 'give_order_form':give_order_form,
            'email':request.user.email,
        }
        return render(request,"giveform.html",context)
    else:
        try:
            #book_form = BookForm(request.POST or None)
            # give_order_form = GiveOrderForm(request.POST or None) 
            #give_form = GiveForm(request.GET or None, initial = {'email':request.user.email})

            context ={
                # 'book_form':book_form,
                # 'give_order_form':give_order_form,
                #'give_form':give_form,
                'email':request.user.email,
            }
            return render(request,"giveform.html",context)
        except:
            return render(request,"home.html")

def BookTakeFormView(request):
    if request.method == "POST":
        context = {
            'email':request.user.email,
            'bookchoices':['a','b','c'],
        }
        return render(request,"takeform.html",context)
    else:
        try:
            context ={
                'email':request.user.email,
                'bookchoices':['a','b','c'],
            }
            return render(request,"takeform.html",context)
        except:
            return render(request,"home.html")


