"""trydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from mainApp import views
from mainApp.views import Messages, RoomView, GroupMessage, EditProfile, MessageScreen
from django.views.generic.base import TemplateView
from django.conf.urls.static import static

from django.conf import settings

urlpatterns = [

                path('admin/', admin.site.urls, name='admin'),

                path('accounts/', include('accounts.urls')),
                path('accounts/', include('django.contrib.auth.urls')),
                # path('', RedirectView.as_view(url='/mainApp/', permanent=True)),
                # url(r'^mainApp/', include('mainApp.urls')),

                url(r'all_rooms/create_rooms/$', RoomView.as_view(), name='create_rooms'),
                path('all_rooms/', RoomView.all_rooms, name='all_rooms'),
                path('messages/', Messages.as_view(), name='messages'),

                url(r'rooms/(?P<slug>[-\w]+)/$', views.RoomView.room_detail, name="rooms"),
                path('', TemplateView.as_view(template_name='home.html'), name='home'),

                url(r'^profile/(?P<user_username>[\w]+)/$', MessageScreen.as_view(), name='profile'),
                url(r'^group_profile/(?P<group_name>[\w]+)/$', GroupMessage.as_view(), name='group_profile'),

                # path('all_rooms/create_rooms/', RoomView.as_view(), name='create_rooms'),
                path('create_group/', GroupMessage.create_group, name='create_group'),
                path('save_group/', views.save_group, name='save_group'),
                path('profile_page/', views.view_profile, name='profile_page'),
                path('edit_profile/', EditProfile.as_view(), name='edit_profile'),



                # path('group_chat/', views.group_chat, name='group_chat'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
