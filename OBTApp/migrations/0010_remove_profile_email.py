# Generated by Django 3.1.2 on 2020-11-27 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OBTApp', '0009_auto_20201127_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
    ]
