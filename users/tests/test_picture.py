from django.contrib.auth.models import User
from django.test import TestCase
from .models import Profile, Relation, ProfilePic

class ProfilePicModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        
        cls.user = User.objects.create_user(username='testuser', password='testpass')

    def test_profile_pic_upload(self):
        profile_pic = ProfilePic.objects.create(user=self.user, profile_pic='uploads/photos/test.jpg')
        self.assertEqual(profile_pic.profile_pic.name, 'uploads/photos/test.jpg')