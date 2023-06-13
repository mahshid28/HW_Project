from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(_("Bio"), max_length=300, blank=True)
    profile_picture = models.ImageField(_("Profile_pic"), upload_to='profile_pics', blank=True)
    phone_number = models.CharField(_("Phone_number"), max_length=20, blank=True)

    class Meta:
        verbose_name = _('Profile')

    def __str__(self):
        return f'{self.user.username} Profile'