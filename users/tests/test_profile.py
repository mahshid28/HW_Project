from django.contrib.auth.models import User
from django.test import TestCase
from .models import Profile, Relation, ProfilePic

class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        
        cls.user = User.objects.create_user(username='testuser', password='testpass')

    def test_bio_label(self):
        profile = Profile.objects.create(user=self.user, bio='Test bio')
        field_label = profile._meta.get_field('bio').verbose_name
        self.assertEqual(field_label, 'Bio')

    def test_phone_number_label(self):
        profile = Profile.objects.create(user=self.user, phone_number='1234567890')
        field_label = profile._meta.get_field('phone_number').verbose_name
        self.assertEqual(field_label, 'Phone_number')

    def test_profile_str(self):
        profile = Profile.objects.create(user=self.user, bio='Test bio')
        expected_str = f'{self.user.username} Profile'
        self.assertEqual(str(profile), expected_str)
