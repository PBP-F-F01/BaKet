from django.test import TestCase
from django.contrib.auth.models import User
from apps.user.models import UserProfile
from datetime import datetime

class UserProfileModelTest(TestCase):

    def setUp(self):
        # Create a sample user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
    
    def test_create_user_profile(self):
        # Ensure a UserProfile can be created and is associated with the user
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.birth_date, datetime(2000, 1, 1))  # Check default birth date
        self.assertIsNone(profile.email)  # Default email should be None
        self.assertIsNone(profile.phone_number)  # Default phone number should be None
        self.assertIsNone(profile.gender)  # Default gender should be None

    def test_update_profile_picture(self):
        # Check if profile picture can be updated
        profile = UserProfile.objects.create(user=self.user)
        profile.profile_picture = 'profile_image/test_image.png'
        profile.save()
        self.assertEqual(profile.profile_picture, 'profile_image/test_image.png')
    
    def test_update_birth_date(self):
        # Update birth date and check if it's saved correctly
        profile = UserProfile.objects.create(user=self.user)
        new_birth_date = datetime(1995, 6, 15)
        profile.birth_date = new_birth_date
        profile.save()
        self.assertEqual(profile.birth_date, new_birth_date)
    
    def test_update_gender(self):
        # Test updating gender and checking choices
        profile = UserProfile.objects.create(user=self.user)
        profile.gender = 'Pria'
        profile.save()
        self.assertEqual(profile.gender, 'Pria')
        
        profile.gender = 'Wanita'
        profile.save()
        self.assertEqual(profile.gender, 'Wanita')
    
    def test_update_email(self):
        # Update email and check if it’s saved correctly
        profile = UserProfile.objects.create(user=self.user)
        profile.email = 'testuser@example.com'
        profile.save()
        self.assertEqual(profile.email, 'testuser@example.com')
    
    def test_update_phone_number(self):
        # Update phone number and check if it’s saved correctly
        profile = UserProfile.objects.create(user=self.user)
        profile.phone_number = '1234567890'
        profile.save()
        self.assertEqual(profile.phone_number, '1234567890')

    def test_str_method(self):
        # Test the __str__ method
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(str(profile), "testuser's profile")
