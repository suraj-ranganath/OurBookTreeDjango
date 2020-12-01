from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    phoneNo=models.CharField(max_length=10)
    location=models.CharField(max_length=1000)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

#This table contains the details of all books.
class Book(models.Model):
    GRADE_S = (
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
    )
    SUBJECT_S = (
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
    )
    grade = models.CharField(max_length=2, choices = GRADE_S)
    '''if grade in ('11', '12'):
        SUBJECT_S = (
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
        )
    elif grade in ('9','10'):
        SUBJECT_S = (
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
        )
    '''
    bookName = models.CharField(max_length=300)
    subject = models.CharField(max_length=2, choices = SUBJECT_S)
#This table contains details of Take Requests.
class Take(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    completedFlag = models.IntegerField(default=0)
#This table contains the details about each taken book. 
class TakeOrder(models.Model):
    takeNo = models.ForeignKey(Take, on_delete=models.CASCADE)
    bookID = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    completedFlag = models.IntegerField(default=0)
#This table contains details of Give Requests.
class Give(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    completedFlag = models.IntegerField(default=0)
#This table contains the details about each given book.
class GiveOrder(models.Model):
    CONDITION_S = (('1' ,'Like new'),
            ('2','Fair'),
            ('3','Pages torn'),
            ('4','Pages missing'),
            ('5','Notes written'),
            )
    giveNo = models.ForeignKey(Give, on_delete=models.CASCADE)
    bookID = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    yearPub = models.CharField(max_length=4)
    condition = models.IntegerField(choices = CONDITION_S)
    completedFlag = models.IntegerField(default=0)


#This table contains feedback.
class Feedback(models.Model):
    SID = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=10000)



