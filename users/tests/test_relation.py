from django.contrib.auth.models import User
from django.test import TestCase
from .models import Profile, Relation, ProfilePic

class RelationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        
        cls.user1 = User.objects.create_user(username='testuser1', password='testpass')
        cls.user2 = User.objects.create_user(username='testuser2', password='testpass')

    def test_relation_str(self):
        relation = Relation.objects.create(from_user=self.user1, to_user=self.user2)
        expected_str = f'{self.user1.username} follows {self.user2.username}'
        self.assertEqual(str(relation), expected_str)

