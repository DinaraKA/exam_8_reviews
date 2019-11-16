from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from accounts.forms import UserCreationForm


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email']
                )
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('webapp:index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', context={'form': form})



