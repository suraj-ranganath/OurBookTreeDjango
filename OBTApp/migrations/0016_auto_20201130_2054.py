# Generated by Django 3.1.2 on 2020-11-30 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OBTApp', '0015_auto_20201130_2040'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Feedback',
        ),
        migrations.DeleteModel(
            name='OurUser',
        ),
    ]
