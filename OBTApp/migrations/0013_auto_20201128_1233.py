# Generated by Django 3.1.2 on 2020-11-28 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OBTApp', '0012_auto_20201128_1228'),
    ]

    operations = [
        migrations.RenameField(
            model_name='give',
            old_name='user_id',
            new_name='userid',
        ),
        migrations.RenameField(
            model_name='take',
            old_name='user_id',
            new_name='userid',
        ),
    ]
