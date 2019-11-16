from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse
from django.views.generic import DetailView, UpdateView

from accounts.forms import UserCreationForm, UserInfoChangeForm, UserPasswordChangeForm
from accounts.models import Profile


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
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('webapp:index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', context={'form': form})


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_object'


class UserInfoChangeView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user_update.html'
    context_object_name = 'user_object'
    form_class = UserInfoChangeForm

    def test_func(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={'pk': self.object.pk})


class UserPasswordChangeView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user_password_change.html'
    form_class = UserPasswordChangeForm
    context_object_name = 'user_object'

    def test_func(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse('accounts:login')

