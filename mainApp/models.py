import datetime
from datetime import datetime

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
from django.contrib.postgres.fields import JSONField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
    image = models.ImageField(upload_to='profile_image', null=True, blank=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class Room(models.Model):

    """Represents chat rooms that users can join"""
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    slug = models.CharField(max_length=50)

    def __str__(self):
        """Returns human-readable representation of the model instance."""
        return self.name


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    friends = models.CharField(blank=True, null=True, max_length=25)
    message = models.CharField(blank=True, null=True, max_length=225)
    status = models.CharField(blank=True, null=True, max_length=225)
    created_at = models.DateTimeField(auto_now=True)
    # pub_date = models.DateTimeField(default=timezone.now(), blank=True)
    date = models.DateTimeField(default=timezone.now, blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    def friend_name(self):
        return self.friends


class GroupChat(models.Model):
    group_name = models.CharField(default="", blank=True, max_length=25)
    date = models.DateTimeField(default=timezone.now, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='authorgroup')
    message = models.CharField(blank=True, null=True, max_length=225)
    is_read = models.BooleanField(default=False)
    # members = models.TextField(null=True)
    # members = ArrayField(models.TextField(max_length=1000), default=list)
    # members = JSONField(default=list)

    def __str__(self):
        return self.group_name


class GroupChatMember(models.Model):
    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, null=True, blank=True)
    member = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.member.username
