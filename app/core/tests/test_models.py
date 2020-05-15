from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Question


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
            username='testsuperuser',
            password='testsuperpass',
            email='admin@company.com'
        )

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_question_success(self):
        """Test creating questions polls"""
        payload = {
            'title': 'How old are you?',
            'type': 'Text response'
        }
        question = Question.objects.create(**payload)

        self.assertEqual(str(question), payload['title'])
