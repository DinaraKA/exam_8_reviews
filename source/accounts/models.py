from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE,
                                verbose_name='User')
    photo = models.ImageField(null=True, blank=True, upload_to='user_photo', verbose_name='Photo')

    def str(self):
        return self.user.get_full_name() + "'s Profile"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

