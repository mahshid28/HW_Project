from django.test import TestCase
from .models import Post

class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(user=self.user, content='test content')
        self.like = Like.objects.create(user=self.user, related_post=self.post)

    def test_true_like(self):
        self.assertTrue(self.post.is_liked_by_user(user))

    def test_user_can_like(self):
        self.assertTrue(self.post.user_can_like(self.user))
        self.assertFalse(self.post.user_can_like(User.objects.create_user(username='testuser2',\
             password='testpass')))