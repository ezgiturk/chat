# Generated by Django 2.1 on 2018-08-29 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0004_auto_20180827_1207'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupchat',
            old_name='create_date',
            new_name='date',
        ),
    ]