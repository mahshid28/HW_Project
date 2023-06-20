from django.contrib.auth.models import User
from django.db import models
from core.models import BaseModel, TimeStampMixin
from django.utils.translation import gettext as _


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(_("Bio"), max_length=300, blank=True)
    #profile_picture = models.ImageField(_("Profile_picture"), upload_to='profile_pics', blank=True)
    phone_number = models.CharField(_("Phone_number"), max_length=11, blank=True)

    class Meta:
        verbose_name = _('Profile')

    def __str__(self):
        return f'{self.user.username} Profile'

class Relation(BaseModel, TimeStampMixin):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    # created_at = models.DateField(auto_now_add=True)
    # updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = _('Profile')

    def __str__(self):
        return f'{self.user.username} Profile'

class ProfilePic(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(_("Profile_picture"), upload_to='uploads/photos/', blank=True)