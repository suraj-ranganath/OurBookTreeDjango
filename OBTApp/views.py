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
from OBTApp import secrets
# Create your views here.
cursor = connection.cursor()
finalentriestake = {}
finalentriesgive = {}
var = {}
filttake = {}
filtgive = {}

def LoggedInHomeView(request):
    
    cursor.execute("select b.grade,b.subject,b.bookname,go.quantity,go.completedFlag from obtapp_giveorder go,obtapp_give g,obtapp_book b where b.id=go.bookID_id and g.id=go.giveNo_id and g.userid_id={}".format(request.user.id))
    bksgiven = cursor.fetchall()
    cursor.execute("select b.grade,b.subject,b.bookname,tko.quantity,tko.completedFlag from obtapp_takeorder tko,obtapp_take t,obtapp_book b where b.id=tko.bookID_id and t.id=tko.takeNo_id and t.userid_id={}".format(request.user.id))
    bkstaken = cursor.fetchall()
    context = {
        'user':request.user,
        'bksgiven':bksgiven,
        'bkstaken':bkstaken,
    }
    
    return render(request,"home.html")

    '''
    if request.method == "POST":
        filters = dict(request.POST)
        filters.pop('csrfmiddlewaretoken')
        for i in filters:
            if 'take' in i:
                filttake[i] = filters[i]
            elif 'give' in key:
                filtgive[i] = filters[i]

        context['bkstaken'] = tuple(i for i in bkstaken if i[1] == filttake['subtake'][0])
        context['filttake'] = filttake
        return render(request,"home.html",context)
    else:
        return render(request,"home.html",context)
    '''

def EmailSend(subject,body,ToEmail):
    gmail_user = 'bookabookasap@gmail.com'
    gmail_password = secrets.obtpassword

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
        global finalentriesgive
        global var
        userid = request.user.id
        entries = request.POST
        print(entries)
        print(finalentriesgive)
        if dict(request.POST).get('action') != ['']:
            if dict(request.POST).get('subject') in (None,'',['']) and dict(request.POST).get('bookname') in (None,'',['']) and dict(request.POST).get('booknameother') in (None,'',['']):

                finalentriesgive['grade'] = entries['grade']

                global SUBJECT_LIST
                SUBJECT_LIST = []
                if entries['grade'] in ('11', '12'):
                    SUBJECT_LIST += [
                        ('M', 'Maths'),
                        ('P', 'Physics'),
                        ('C', 'Chemistry'),
                        ('CS', 'Computer Science'),
                        ('B', 'Biology'),
                        ('E', 'English'),
                        ('A','Accountancy'),
                        ('EC','Economics'),
                        ('BS','Business Studies'),
                        ('EN','Entrepreneurship'),
                        ('H','History'),
                        ('SO','Sociology'),
                        ('PS','Psychology'),
                    ]
                elif entries['grade'] in ('9','10'):
                    SUBJECT_LIST += [
                        ('M', 'Maths'),
                        ('P', 'Physics'),
                        ('C', 'Chemistry'),
                        ('CS', 'Computer Science'),
                        ('B', 'Biology'),
                        ('E', 'English'),
                        ('S','Sanskrit'),
                        ('SS','Social Studies'),
                        ('HI','Hindi'),
                        ('K','Kannada'),
                        ('F','French'),
                        ('G','German'),
                    ]

                context = {
                'email':request.user.email,
                'grade':finalentriesgive['grade'],
                'sublist':SUBJECT_LIST,
                }
                return render(request,"giveform.html",context)

            elif dict(request.POST).get('bookname') in (None,'',['']) and dict(request.POST).get('booknameother') in (None,'',['']):

                finalentriesgive['subject'] = entries['subject']
                cursor.execute("select distinct bookName from obtapp_book where subject='{}' and grade={}".format(finalentriesgive['subject'],finalentriesgive['grade']))
                allbooks = cursor.fetchall()
                var['allbooks'] = allbooks
                context = {
                'email':request.user.email,
                'bookchoices':allbooks,
                'grade':finalentriesgive['grade'],
                'sublist':SUBJECT_LIST,
                'sub':finalentriesgive['subject']
                }
                return render(request,"giveform.html",context)
            elif dict(request.POST).get('bookname') == ["Other"] and dict(request.POST).get('booknameother') in (None,'',['']):
                # cursor.execute("select distinct bookName from obtapp_book where subject='{}' and grade={}".format(finalentriesgive['subject'],finalentriesgive['grade']))
                # allbooks = cursor.fetchall()
                context = {
                'email':request.user.email,
                'bookchoices':var['allbooks'],
                'grade':finalentriesgive['grade'],
                'sublist':SUBJECT_LIST,
                'sub':finalentriesgive['subject'],
                'otherflag':True,
                'book':"Other..",
                }
                return render(request,"giveform.html",context)
            elif entries['bookname'] != ['Other']:
                finalentriesgive['bookname'] = entries['bookname']
                context = {
                'email':request.user.email,
                'bookchoices':var['allbooks'],
                'grade':finalentriesgive['grade'],
                'sublist':SUBJECT_LIST,
                'sub':finalentriesgive['subject'],
                'book':finalentriesgive['bookname'],
                }
                return render(request,"giveform.html",context)
        else:

            finalentriesgive['quan'] = entries['quan']
            finalentriesgive['yearpub'] = entries['yearpub']
            finalentriesgive['condition'] = entries['condition']
            if dict(request.POST).get('booknameother') != None:
                finalentriesgive['bookname'] = entries['booknameother']
            print(finalentriesgive)
            cursor.execute("insert into obtapp_book (grade,bookName,subject) values ('{}','{}','{}')".format(finalentriesgive['grade'],finalentriesgive['bookname'],finalentriesgive['subject']))
            cursor.execute("insert into obtapp_give (userid_id,completedFlag) values ('{}',0)".format(userid))
            cursor.execute("select id from obtapp_book where id=(select max(id) from obtapp_book)") #find better way
            bookid=cursor.fetchall()[0][0]
            cursor.execute("select id from obtapp_give where id=(select max(id) from obtapp_give) and userid_id = {}".format(userid))
            giveno=cursor.fetchall()[0][0]
            cursor.execute("insert into obtapp_giveorder (quantity,yearPub,`condition`,completedFlag,bookID_id,giveNo_id) values ({},'{}','{}',0,{},{})".format(finalentriesgive['quan'],finalentriesgive['yearpub'],finalentriesgive['condition'],bookid,giveno))

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
        global finalentriestake
        
        entries = request.POST
        if dict(request.POST).get('subject') in (None,'',['']) and dict(request.POST).get('bookname') in (None,'',['']):
            finalentriestake['grade'] = entries['grade']
            
            global SUBJECT_LIST
            SUBJECT_LIST = []
            if entries['grade'] in ('11', '12'):
                SUBJECT_LIST += [
                    ('M', 'Maths'),
                    ('P', 'Physics'),
                    ('C', 'Chemistry'),
                    ('CS', 'Computer Science'),
                    ('B', 'Biology'),
                    ('E', 'English'),
                    ('A','Accountancy'),
                    ('EC','Economics'),
                    ('BS','Business Studies'),
                    ('EN','Entrepreneurship'),
                    ('H','History'),
                    ('SO','Sociology'),
                    ('PS','Psychology'),
                ]
            elif entries['grade'] in ('9','10'):
                SUBJECT_LIST += [
                    ('M', 'Maths'),
                    ('P', 'Physics'),
                    ('C', 'Chemistry'),
                    ('CS', 'Computer Science'),
                    ('B', 'Biology'),
                    ('E', 'English'),
                    ('S','Sanskrit'),
                    ('SS','Social Studies'),
                    ('HI','Hindi'),
                    ('K','Kannada'),
                    ('F','French'),
                    ('G','German'),
                ]

            context = {
            'email':request.user.email,
            'grade':finalentriestake['grade'],
            'sublist':SUBJECT_LIST,
            }
            return render(request,"takeform.html",context)
        elif dict(request.POST).get('bookname') in (None,'',['']):
            finalentriestake['subject'] = entries['subject']
            cursor.execute("select distinct bookName from obtapp_book where subject='{}' and grade={}".format(finalentriestake['subject'],finalentriestake['grade']))
            allbooks = cursor.fetchall()

            context = {
            'email':request.user.email,
            'bookchoices':allbooks,
            'sub':finalentriestake['subject'],
            'grade':finalentriestake['grade'],
            'sublist':SUBJECT_LIST,
            }
            return render(request,"takeform.html",context)
        else:
            finalentriestake['bookname'] = entries['bookname']
            finalentriestake['quan'] = entries['quan']

            userid = request.user.id
            cursor.execute("insert into obtapp_take (userid_id,completedFlag) values ('{}',0)".format(userid))
            cursor.execute("select id from obtapp_book where grade = {} and subject = '{}' and bookname = '{}'".format(finalentriestake['grade'],finalentriestake['subject'],finalentriestake['bookname']))
            bookid = cursor.fetchall()[0][0]

            cursor.execute("select id from obtapp_take where id=(select max(id) from obtapp_take) and userid_id = {}".format(userid))
            takeno = cursor.fetchall()[0][0]
            cursor.execute("insert into obtapp_takeorder (takeNo_id,bookID_id,quantity,completedFlag) values ({},{},{},0)".format(takeno,bookid,finalentriestake['quan']))
            
            context = {
            'email':request.user.email,
            }
            return render(request,"takeform.html",context)

        
    else:
        try:
            context ={
                'email':request.user.email,
            }
            return render(request,"takeform.html",context)
        except:
            return render(request,"home.html")



