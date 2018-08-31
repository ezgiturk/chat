from django.contrib import admin
from .models import Room, Conversation, UserProfile, GroupChat

admin.site.register(Room)
admin.site.register(GroupChat)
admin.site.register(Conversation)
admin.site.register(UserProfile)
# Register your models here.