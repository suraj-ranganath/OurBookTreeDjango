# Generated by Django 3.1.2 on 2020-11-17 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OBTApp', '0002_auto_20201117_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giveorder',
            name='yearPub',
            field=models.CharField(max_length=4),
        ),
    ]
