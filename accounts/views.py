from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from mainApp.forms import SignUpForm


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login')

    else:
        form = SignUpForm()

        args = {'form': form}
        return render(request, 'signup.html', args)

    return redirect('/accounts/login')