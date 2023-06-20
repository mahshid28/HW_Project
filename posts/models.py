from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel, TimeStampMixin
from django.utils.translation import gettext as _
from django.utils import timezone

class Post(TimeStampMixin, BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(_("Content"), max_length=1000)

    def is_liked_by_user(self,user):
        return self.like_set.filter(user=user).exists()

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _("Posts")

    def __str__(self):
        return f'{self.user.username} - {self.created_at}'

class Comment(BaseModel, TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    related_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(_("Content"), max_length=500, blank=True, null=True)
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def get_user(self):
        return self.user

    def get_post(self):
        return self.related_post

    @staticmethod
    def get_comments_for_post(post):
        return Comment.objects.filter(related_post=post)

    def is_editable(self):
        edit_time_limit = timezone.now() - timezone.timedelta(minutes=10)
        if self.updated_at is None:
            return True
        else:
            updated_at_local = timezone.localtime(make_aware(self.updated_at))
            return updated_at_local < edit_time_limit

    def edit_comment(self, user, new_content):
        if self.user == user and self.is_editable():
            self.content = new_content
            self.updated_at = timezone.now()
            self.save()
        elif self.user != user:
            raise PermissionError("You are not authorized to edit this comment.")
        else:
            raise ValueError("Comment cannot be edited after 10 minutes.")

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f'{self.user.username} - {self.related_post} - {self.content}'

class Like(BaseModel, TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    related_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def get_user(self):
        return self.user

    def get_post(self):
        return self.related_post

    @staticmethod
    def get_likes_count(post):
        return Like.objects.filter(related_post=post).count()

    @staticmethod
    def get_likes_by_user(user):
        likes = Like.objects.filter(user=user).select_related('related_post')
        posts = [like.related_post for like in likes]
        return posts

    class Meta:
        verbose_name = _('Like')
        verbose_name_plural = _("Likes")

    def __str__(self):
        return f'{self.user.username} - {self.related_post}'

class PostImage(BaseModel):
    related_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/photos/')

    class Meta:
        verbose_name = _('Like')
        verbose_name_plural = _("Likes")

    def __str__(self):
        return f'{self.related_post}'

class Tag(BaseModel):
    name = models.CharField(max_length=50)
    related_post = models.ManyToManyField(Post, related_name='tags')

    @staticmethod
    def get_posts_by_tag_name(tag_name):
        return Post.objects.filter(tags__name=tag_name)
