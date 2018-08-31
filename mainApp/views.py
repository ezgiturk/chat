from django.contrib.auth.models import User
import json
import random
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, View

from mainApp.forms import MessagesForm, RoomForm, GroupForm, ProfileForm
from mainApp.models import Room, Conversation, GroupChat, UserProfile, GroupChatMember


class RoomView(View):
    model = Room

    def get(self, request):
        form = RoomForm()
        rooms = Room.objects.all()
        return render(request, 'create_room.html', {'form': form, 'rooms': rooms})

    def post(self, request):
        form = RoomForm(request.POST)
        if form.is_valid():
            room = Room()
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            slug = form.cleaned_data['slug']
            # hh
            room.name = name
            room.description = description
            room.slug = slug
            room.save()

        else:
            return HttpResponse('Form is not valid')

        rooms = Room.objects.all()

        return render(request, 'create_room.html', {'form': form, 'rooms': rooms})

    def all_rooms(request):
        rooms = Room.objects.all()
        return render(request, 'index.html', {'rooms': rooms})

    def room_detail(request, slug):
        room = Room.objects.filter(slug=slug)
        return render(request, 'room_detail.html', {'room': room})


class MessageScreen(View):
    model = Conversation
    template_name = 'message_screen.html'

    def get(self, request, **kwargs):
        form = MessagesForm(request.GET)
        friend_name = kwargs['user_username']
        user = request.user

        others_message = Conversation.objects.filter(Q(user=User.objects.get(username=friend_name)) & Q(friends=user.username))

        for data in others_message:
            data.is_read = True
            data.save()
        all_users = User.objects.all()
        new_message_count = others_message.filter(is_read=False).count()

        groups = GroupChatMember.objects.filter(member=request.user)
        context = {}

        for person in all_users:
            number_not_read = Conversation.objects.filter(Q(user=person) & Q(friends=user.username) & Q(is_read=False)).count()
            context.update({
                person.username: number_not_read
            })
        last_message = Conversation.objects.filter(Q(friends=user.username) & Q(is_read=False)).first()
        old_message = Conversation.objects.order_by('-date').filter(friends=user.username).first()
        print(last_message)
        print(old_message)
        print("buuu")
        mesajlar = Conversation.objects.filter((Q(user=user) & Q(friends=friend_name)) | (
                Q(user=User.objects.get(username=friend_name)) & Q(friends=user.username)))
        mesajlar = mesajlar.order_by('date')

        user_profile = UserProfile.objects.get(user=request.user)

        args = {'form': form, 'mesajlar': mesajlar, 'context': context, 'all_users': all_users, 'groups': groups,
                'last_message': last_message, 'old_message': old_message, 'friend_name': friend_name, 'user_profile': user_profile,
                'new_message_count': new_message_count}

        return render(request, self.template_name, args)

    def post(self, request, **kwargs):
        friend_name = kwargs['user_username']

        form = MessagesForm(request.POST)
        if form.is_valid():
            print("XSXSXSXS")
            conversation = Conversation()
            text = form.cleaned_data['message']

            if request.user.is_authenticated:
                user = request.user
                conversation.user = user
            conversation.message = text
            conversation.friends = friend_name
            conversation.save()

            mesajlar = Conversation.objects.filter((Q(user=user) & Q(friends=friend_name)) | (
                    Q(user=User.objects.get(username=friend_name)) & Q(friends=user.username)))
            mesajlar = mesajlar.order_by('date')
            all_users = User.objects.all()
            args = {'form': form, 'mesajlar': mesajlar, 'all_users': all_users, 'friend_name': friend_name}
            return render(request, self.template_name, args)

        else:
            return redirect('profile', user_username=friend_name)


def view_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    args = {'user_profile': user_profile, 'user': request.user}
    return render(request, 'profile_page.html', args)


class EditProfile(View):
    model = UserProfile
    template_name = 'edit_profile.html'

    def get(self, request):

        form = ProfileForm(instance=request.user.userprofile)
        return render(request, 'edit_profile.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            user = request.user

        form = ProfileForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            description = form.cleaned_data['description']
            city = form.cleaned_data['city']
            website = form.cleaned_data['website']
            phone = form.cleaned_data['phone']

            profile = UserProfile.objects.get(user=request.user)
            profile.user = request.user
            profile.description = description
            profile.city = city
            profile.website = website
            profile.phone = phone

            if 'image' in request.FILES:
                image = request.FILES['image']
                profile.image = image
            profile.save()

        else:
            return HttpResponse('Form is not valid')

        args = {'form': form}
        return render(request, 'edit_profile.html', args)


def save_group(request):
    if request.method == 'POST':
        friends = request.POST.getlist('users[]')
        group_name = request.POST.getlist('group_name')[0]

        friends.append(request.user.username)
        group_chat = GroupChat()
        group_chat.group_name = group_name
        group_chat.user = request.user
        group_chat.save()

        for friend in friends:
            group_chat_member = GroupChatMember()
            group_chat_member.member = User.objects.get(username=friend)
            group_chat_member.chat = group_chat
            group_chat_member.save()
            print(type(group_chat_member.member))
            print(group_chat_member.member)

        mesajlar = GroupChat.objects.filter(group_name=group_name)
        mesajlar = mesajlar.order_by('date')

        return render(request, 'group_chat.html', {'friends': friends, 'mesajlar': mesajlar, 'group_name': group_name})
    else:
        return HttpResponse("sorry")


class GroupMessage(View):
    model = GroupChat
    template_name = 'group_message_screen.html'

    def create_group(request):
        all_user = User.objects.all()
        return render(request, 'create_group.html', {'all_user': all_user})

    def get(self, request, **kwargs):
        form = MessagesForm(request.GET)
        group_name = kwargs['group_name']
        user = request.user
        mesajlar = GroupChat.objects.filter(group_name=group_name)
        # friends = GroupChatMember.objects.filter(GroupChat.objects.filter(group_name=group))
        all_users = User.objects.all()
        return render(request, self.template_name,
                      {'form': form, 'mesajlar': mesajlar, 'all_users': all_users, 'group_name': group_name})

    def post(self, request, **kwargs):
        form = MessagesForm(request.POST)
        group_name = kwargs['group_name']

        if form.is_valid():
            group_chat = GroupChat()
            group_chat_member = GroupChatMember()
            message = form.cleaned_data['message']

            if request.user.is_authenticated:
                user = request.user
                group_chat_member.chat.user = user

            group_chat.message = message
            group_chat.group_name = group_name

            group_chat_member.chat = group_chat
            group_chat.save()
            group_chat_member.save()

            mesajlar = GroupChat.objects.filter(group_name=group_name)
            mesajlar = mesajlar.order_by('date')
            all_users = User.objects.all()
            return render(request, self.template_name,
                          {'form': form, 'mesajlar': mesajlar, 'all_users': all_users, 'group_name': group_name})

        else:
            return redirect('group_profile', group_name=group_name)


class Messages(View):
    model = Conversation
    template_name = 'chat2.html'

    def get(self, request, ):
        form = MessagesForm()
        context = {}
        if request.user.is_authenticated:
            user = request.user
        all_user = User.objects.all()
        # groups = GroupChat.objects.filter(Q(GroupChatMember.objects.get(member=request.user)) | Q(user=request.user))
        # members = GroupChatMember.objects.filter(member=request.user)
        # groups = GroupChat.objects.filter(Q(members) | Q(user=request.user))
        groups = GroupChatMember.objects.filter(member=request.user)
        for group in groups:
            print(group.chat.group_name)

        for person in all_user:
            data = Conversation.objects.filter(Q(user=person) & Q(friends=user.username) & Q(is_read=False)).count()
            context.update({
                person.username: data
            })
        print(context)
        return render(request, self.template_name,
                      {'form': form, 'all_user': all_user, 'context': context, 'groups': groups})



# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.refresh_from_db()  # load the profile instance created by the signal
#             user.profile.birth_date = form.cleaned_data.get('birth_date')
#             user.save()
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=user.username, password=raw_password)
#             login(request, user)
#             return redirect('all_rooms')
#     else:
#         form = SignUpForm()
#     return render(request, 'signup.html', {'form': form})


# def home(request, room_id=None):
#     user = request.GET.get('user')
#     if user:
#         if not room_id:
#             return redirect('/default?' + request.GET.urlencode())
#
#         try:
#             room = ChatRoom.objects.get(eid=room_id)
#             cmsgs = ChatMessage.objects.filter(
#                 room=room).order_by('-date')[:50]
#             msgs = []
#             for msg in reversed(cmsgs):
#                 msgs.append(msg.to_data())
#         except ChatRoom.DoesNotExist:
#             msgs = []
#
#         context = {}
#         context['room_id'] = room_id
#         context['messages'] = msgs
#         context['user'] = user
#         return render(request, 'chat2.html', context)
#     else:
#         context = {}
#         context['room_id'] = room_id or 'default'
#         return render(request, 'index.html', context)
#
#
# def messages(request, room_id):
#     if request.method == 'POST':
#         try:
#             room = ChatRoom.objects.get(eid=room_id)
#         except ChatRoom.DoesNotExist:
#             try:
#                 room = ChatRoom(eid=room_id)
#                 room.save()
#             except IntegrityError:
#                 # someone else made the room. no problem
#                 room = ChatRoom.objects.get(eid=room_id)
#
#         mfrom = request.POST['from']
#         text = request.POST['text']
#         msg = ChatMessage(room=room, user=mfrom, text=text)
#         msg.save()
#         body = json.dumps(msg.to_data())
#         return HttpResponse(body, content_type='application/json')
#     else:
#         return HttpResponseNotAllowed(['POST'])
#
