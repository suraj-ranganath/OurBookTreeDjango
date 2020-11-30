from django.shortcuts import render, redirect
import smtplib
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
def EmailSend(subject,body,ToEmail):
    gmail_user = 'bookabookasap@gmail.com'
    gmail_password = 'ankithsucks'

    sent_from = gmail_user
    to = [ToEmail]

    email_text = """\
    From: %s\nTo: %s\nSubject: %s\n%s

    """ % (sent_from, ", ".join(to), subject, body)

    server1 = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server1.ehlo()
    server1.login(gmail_user, gmail_password)
    server1.sendmail(sent_from, to, email_text)
    server1.close() 

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            #user.refresh_from_db()
            global location11
            global phone11
            location11 = form.cleaned_data.get('location')
            phone11 = form.cleaned_data.get('phoneNo')
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Our Book Tree Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            EmailSend(subject, message, user.email)
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
        user.refresh_from_db()  # load the profile instance created by the signal
        user.is_active = True
        user.profile.email_confirmed = True
        user.profile.location = location11
        user.profile.phoneNo = phone11
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')

def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

def BookGiveFormView(request):
    if request.method == 'POST':

        userid = request.user.id
        entries = request.POST

        cursor.execute("insert into obtapp_book (grade,bookName,subject) values ('{}','{}','{}')".format(entries['grade'],entries['bookname'],entries['subject']))
        cursor.execute("insert into obtapp_give (userid_id,completedFlag) values ('{}',0)".format(userid))
        cursor.execute("select id from obtapp_book where id=(select max(id) from obtapp_book)") #find better way
        bookid=cursor.fetchall()[0][0]
        cursor.execute("select id from obtapp_give where id=(select max(id) from obtapp_give) and userid_id = {}".format(userid))
        giveno=cursor.fetchall()[0][0]
        cursor.execute("insert into obtapp_giveorder (quantity,yearPub,`condition`,completedFlag,bookID_id,giveNo_id) values ({},'{}','{}',0,{},{})".format(entries['quan'],entries['yearpub'],entries['condition'],bookid,giveno))
        
        # saving data to db using django forms 
        '''
        book_form = BookForm()
        give_order_form = GiveOrderForm()   

        give_form = GiveForm(request.POST or None,initial={'email':request.user.email})
        
        if give_order_form.is_valid() and book_form.is_valid():
            book = book_form.save()
            give_order = give_order_form.save(False)    

            give = Give(email=request.user.email)
            give.save()
            give = give_form.save()

            give_order.bookID = book
            give_order.save()
            give_order.giveNo = give 
            book_form = BookForm()
            give_order_form = GiveOrderForm()
        '''
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
                # 'give_form':give_form,
                'email':request.user.email,
            }
            return render(request,"giveform.html",context)
        except:
            return render(request,"home.html")

def BookTakeFormView(request):
    if request.method == "POST":

        userid = request.user.id
        entries = request.POST
        
        cursor.execute("insert into obtapp_take (userid_id,completedFlag) values ('{}',0)".format(userid))
        cursor.execute("select id from obtapp_book where grade = {} and subject = '{}' and bookname = '{}'".format(entries['grade'],entries['subject'],entries['bookname']))
        bookid = cursor.fetchall()[0][0]
        print(bookid)
        cursor.execute("select id from obtapp_take where id=(select max(id) from obtapp_take) and userid_id = {}".format(userid))
        takeno = cursor.fetchall()[0][0]
        cursor.execute("insert into obtapp_takeorder (takeNo_id,bookID_id,quantity,completedFlag) values ({},{},{},0)".format(takeno,bookid,entries['quan']))



        context = {
            'email':request.user.email,
            'bookchoices':['a','b','c'],
        }
        return render(request,"takeform.html",context)
    else:
        try:
            context ={
                'email':request.user.email,
                'bookchoices':['a','b','c','RD Sharma'],
            }
            return render(request,"takeform.html",context)
        except:
            return render(request,"home.html")

def getdetails(request):
    subject = request.GET['cnt1']
    print ("ajax subject ", subject)
    result_set = []
    all_books = []
    answer = str(subject[1:-1])
    selected_subject = allsubjects.objects.get(name=answer)
    print ("selected subject ", selected_subject)
    # all_chapters = selected_subject.chapter123_set.all()
    # for chapter in all_chapters:
        # print ("chapter", chapter.name)
        # result_set.append({'name': chapter.name})
    # return HttpResponse(simplejson.dumps(result_set),content_type='application/json')


