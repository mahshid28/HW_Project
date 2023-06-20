from django.test import TestCase
from django.contrib.auth.models import User
from posts.models import Post, Comment, Like, Tag

class TagTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post1 = Post.objects.create(user=self.user, content='test content 1')
        self.post2 = Post.objects.create(user=self.user, content='test content 2')
        self.tag1 = Tag.objects.create(name='food')
        self.tag2 = Tag.objects.create(name='travel')
        self.post1.tags.add(self.tag1)
        self.post2.tags.add(self.tag2)

    def test_get_posts_by_tag_name(self):
        food_posts = Tag.objects.get(name='food').get_posts_by_tag_name('food')
        self.assertEqual(food_posts.count(), 1)
        self.assertEqual(food_posts.first(), self.post1)
        
        travel_posts = Tag.objects.get(name='travel').get_posts_by_tag_name('travel')
        self.assertEqual(travel_posts.count(), 1)
        self.assertEqual(travel_posts.first(), self.post2)