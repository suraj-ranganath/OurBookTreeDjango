# Generated by Django 3.1.2 on 2020-11-28 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OBTApp', '0011_auto_20201128_1218'),
    ]

    operations = [
        migrations.RenameField(
            model_name='give',
            old_name='email',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='take',
            old_name='email',
            new_name='user_id',
        ),
    ]
