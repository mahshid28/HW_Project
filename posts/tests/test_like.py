from django.test import TestCase
from django.contrib.auth.models import User
from posts.models import Post, Like

class LikeTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass')
        self.post1 = Post.objects.create(user=self.user1, content='test content 1')
        self.post2 = Post.objects.create(user=self.user2, content='test content 2')
        self.like1 = Like.objects.create(user=self.user1, related_post=self.post1)
        self.like2 = Like.objects.create(user=self.user2, related_post=self.post2)

    def test_get_user(self):
        user1 = self.like1.get_user()
        user2 = self.like2.get_user()
        self.assertEqual(user1, self.user1)
        self.assertEqual(user2, self.user2)

    def test_get_post(self):
        post1 = self.like1.get_post()
        post2 = self.like2.get_post()
        self.assertEqual(post1, self.post1)
        self.assertEqual(post2, self.post2)

    def test_get_likes_count(self):
        likes_count1 = Like.get_likes_count(self.post1)
        likes_count2 = Like.get_likes_count(self.post2)
        self.assertEqual(likes_count1, 1)
        self.assertEqual(likes_count2, 1)

    def test_get_likes_by_user(self):
        likes1 = Like.get_likes_by_user(self.user1)
        likes2 = Like.get_likes_by_user(self.user2)
        likes3 = Like.get_likes_by_user(User.objects.create_user(username='testuser3', password='testpass'))
        self.assertEqual(len(likes1), 1)
        self.assertIn(self.post1, likes1)
        self.assertIn(self.post2, likes2)
        self.assertEqual(len(likes2), 1)
        self.assertIn(self.post2, likes2)
        self.assertEqual(len(likes3), 0)
        self.assertEqual(likes3, [])
