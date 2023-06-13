from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(_("Content"), max_length=1000)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _("Posts")

    def __str__(self):
        return f'{self.user.username} - {self.created_at}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(_("Content"), max_length=500)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f'{self.user.username} - {self.post} - {self.created_at}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    class Meta:
        verbose_name = _('Like')
        verbose_name_plural = _("Likes")

    def __str__(self):
        return f'{self.user.username} - {self.post} - {self.created_at}'