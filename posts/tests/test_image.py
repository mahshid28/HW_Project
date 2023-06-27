from django.test import TestCase
from django.contrib.auth.models import User
from posts.models import Post

class PostImageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(user=self.user, content='test content')
        self.image = PostImage.objects.create(image='test.jpg', related_post=self.post)

    def test_related_post(self):
        self.assertEqual(self.image.related_post, self.post)

    def test_save_method(self):
        self.assertTrue(self.image.image.storage.exists(self.image.image.name))
        self.assertTrue(self.image.thumbnail.storage.exists(self.image.thumbnail.name))

    def test_delete_method(self):
        self.image.delete()
        self.assertFalse(self.image.image.storage.exists(self.image.image.name))
        self.assertFalse(self.image.thumbnail.storage.exists(self.image.thumbnail.name))

    def test_get_thumbnail_url_method(self):
        url = self.image.get_thumbnail_url()
        self.assertTrue(url.endswith('thumbnail.jpg'))