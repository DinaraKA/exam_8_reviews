from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import widgets

from accounts.models import Profile


class UserCreationForm(forms.Form):
    username = forms.CharField(max_length=20, label='Username', required=True)
    password = forms.CharField(max_length=20, min_length=8, label='Password', required=True,
                               widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=20, min_length=8, label='Password Comfirm', required=True,
                               widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', required=True)


    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
            raise ValidationError('User with this email already exists',
                                  code='user_email_exists')
        except User.DoesNotExist:
            return email

    def clean_username(self):
        username=self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
            raise ValidationError('User with this username already exists',
                              code='user_username_exists')
        except User.DoesNotExist:
            return username

    def clean_password_confirmn(self):
        super().clean()
        password_1 = self.cleaned_data['password']
        password_2 = self.cleaned_data['password_confirm']
        if password_1 != password_2:
            raise ValidationError('Passwords do not match',
                                  code='passwords_do_not_match')
        return password_2


    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email']


class UserInfoChangeForm(forms.ModelForm):
    photo = forms.ImageField(label='Avatar', required=False)

    def get_initial_for_field(self, field, field_name):
        if field_name in self.Meta.profile_fields:
            return getattr(self.instance.profile, field_name)
        return super().get_initial_for_field(field, field_name)

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.profile = self.save_profile(commit)
        return user

    def save_profile(self, commit=True):
        profile, _ = Profile.objects.get_or_create(user=self.instance)
        for field in self.Meta.profile_fields:
            setattr(profile, field, self.cleaned_data.get(field))
        if commit:
            profile.save()
        return profile



    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        profile_fields =['photo']
