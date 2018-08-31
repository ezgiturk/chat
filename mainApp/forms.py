from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from mainApp.models import Conversation, Room, GroupChat, UserProfile


class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'birth_date',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class LoginForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')


class MessagesForm(forms.ModelForm):
    # username = forms.CharField(widget=forms.TextInput())
    message = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = Conversation
        fields = ('message',)


class RoomForm(forms.ModelForm):
    # name = forms.CharField(widget=forms.TextInput())
    # description = forms.CharField(widget=forms.TextInput)
    # slug = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = Room
        fields = ('name', 'description', 'slug',)


class GroupForm(forms.ModelForm):
    message = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = GroupChat
        fields = ('group_name', 'message',)


class ProfileForm(forms.ModelForm):
    description = forms.CharField(max_length=100, widget=forms.Textarea())
    city = forms.CharField(max_length=100)
    website = forms.URLField()
    phone = forms.IntegerField()
    image = forms.ImageField()

    class Meta:
        model = UserProfile
        fields = ('description',
                  'city',
                  'website',
                  'phone',
                  'image',
                  )

    # def save(self, commit=True):
    #     user = super(ProfileForm, self).save(commit=False)
    #     user.description = self.cleaned_data['description']
    #     user.website = self.cleaned_data['website']
    #     user.city = self.cleaned_data['city']
    #     user.phone = self.cleaned_data['phone']
    #     # user.image = self.cleaned_data['image']
    #
    #     if commit:
    #         user.save()
    #
    #     return user