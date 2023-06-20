from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from posts.models import Post, Comment

class CommentTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass')
        self.post1 = Post.objects.create(user=self.user1, content='test content 1')
        self.post2 = Post.objects.create(user=self.user1, content='test content 2')
        self.comment1 = Comment.objects.create(user=self.user1, related_post=self.post1, content='test comment 1')
        self.comment2 = Comment.objects.create(user=self.user2, related_post=self.post1, content='test comment 2')
        self.comment3 = Comment.objects.create(user=self.user1, related_post=self.post2, content='test comment 3')

    def test_get_user(self):
        self.assertEqual(self.comment1.get_user(), self.user1)
        self.assertEqual(self.comment2.get_user(), self.user2)
        self.assertEqual(self.comment3.get_user(), self.user1)

    def test_get_post(self):
        self.assertEqual(self.comment1.get_post(), self.post1)
        self.assertEqual(self.comment2.get_post(), self.post1)
        self.assertEqual(self.comment3.get_post(), self.post2)

    def test_get_comments_for_post(self):
        comments1 = Comment.get_comments_for_post(self.post1)
        comments2 = Comment.get_comments_for_post(self.post2)
        self.assertEqual(len(comments1), 2)
        self.assertIn(self.comment1, comments1)
        self.assertIn(self.comment2, comments1)
        self.assertEqual(len(comments2), 1)
        self.assertIn(self.comment3, comments2)

    def test_is_editable(self):
        create_time = datetime.strptime(str(self.comment1.created_at), '%Y-%m-%d %H:%M:%S.%f')
        self.comment1.updated_at = create_time - timezone.timedelta(minutes=11)
        self.assertFalse(self.comment1.is_editable())

        self.comment1.updated_at = None
        self.assertTrue(self.comment1.is_editable())

        self.comment1.updated_at = timezone.now() - timezone.timedelta(minutes=5)
        self.assertTrue(self.comment1.is_editable())

    def test_edit_comment(self):
        self.comment1.edit_comment(self.user1, "This is the updated comment content.")
        self.assertEqual(self.comment1.content, "This is the updated comment content.")

        with self.assertRaises(PermissionError):
            self.comment2.edit_comment(self.user1, "This is the updated comment content.")

        self.comment1.updated_at = self.comment1.created_at - timezone.timedelta(minutes=11)
        with self.assertRaises(ValueError):
            self.comment1.edit_comment(self.user1, "This is the updated comment content.")