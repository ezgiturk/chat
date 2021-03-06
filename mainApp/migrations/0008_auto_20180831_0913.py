# Generated by Django 2.1 on 2018-08-31 09:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0007_auto_20180830_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupchatmember',
            name='chat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.GroupChat'),
        ),
        migrations.AlterField(
            model_name='groupchatmember',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
