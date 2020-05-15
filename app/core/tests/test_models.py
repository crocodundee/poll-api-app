from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelsTests(TestCase):
    """Testing project's models"""

    def test_create_user_success(self):
        """Test create user with valid credentials"""
        username = 'testuser'
        password = 'testpass'
        user = get_user_model().objects.create_user(
            username=username,
            password=password
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_create_superuser(self):
        """Test is superuser created successfull"""
        superuser = get_user_model().objects.create_superuser(
            'testsuperuser', 'testsuperpass'
        )

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
