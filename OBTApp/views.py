from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .forms import *
from .models import *
from django.db import connection
from django.contrib.auth.forms import UserCreationForm
from django.utils.encoding import force_text
from django.contrib.auth import login, authenticate
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from OBTApp.tokens import account_activation_token
# Create your views here.
cursor = connection.cursor()


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Our Book Tree Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')

def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

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




