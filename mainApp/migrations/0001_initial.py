# Generated by Django 2.1 on 2018-08-27 09:21

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friends', models.CharField(blank=True, max_length=25, null=True)),
                ('message', models.CharField(blank=True, max_length=225, null=True)),
                ('status', models.CharField(blank=True, max_length=225, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('is_read', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GroupChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(blank=True, max_length=25, null=True)),
                ('create_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('message', models.CharField(blank=True, max_length=225, null=True)),
                ('is_read', models.BooleanField(default=False)),
                ('members', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(max_length=200), default=list, size=None)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='authorgroup', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='', max_length=100)),
                ('city', models.CharField(default='', max_length=100)),
                ('website', models.URLField(default='')),
                ('phone', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, upload_to='profile_image')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]