from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Poll, Question
from poll.serializers import PollCrudSerializer


POLL_URL = reverse('poll:poll-list')


def detail_url(poll_id):
    """Create and return detail poll url"""
    return reverse('poll:poll-detail', args=[poll_id])


def sample_question(user, title='Sample question', type='TEXT'):
    """Create base question"""
    return Question.objects.create(user=user, title=title, type=type)


class PollEndpointCRUDTests(TestCase):
    """Test CRUD poll's operations provide by admin"""

    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            username='admin',
            password='adminpass',
            email='admin@company.com'
        )
        self.client.force_authenticate(user=self.admin)

    def test_create_poll(self):
        """Test admin can create poll"""
        payload = {
            'title': 'Profile poll',
            'description': "Get user's personal info",
            'date_start': '2020-05-15',
            'date_end': '2020-05-22'
        }
        res = self.client.post(POLL_URL, payload)

        self.assertEqual(res.status_code, status. HTTP_201_CREATED)

        poll = Poll.objects.get(title=payload['title'])
        serializer = PollCrudSerializer(poll)

        self.assertEqual(res.data, serializer.data)

    def test_update_poll(self):
        """Test admin can update poll"""
        poll = Poll.objects.create(
            title='Profile poll',
            description='Get personal info',
            date_start='2020-05-15',
            date_end='2020-05-22',
            user=self.admin
        )
        q1 = sample_question(user=self.admin, title='Question 1')
        q2 = sample_question(user=self.admin, title='Question 2')

        payload = {
            'title': 'Profile info',
            'questions': [q1.id, q2.id],
            'date_end': '2020-06-15'
        }

        url = detail_url(poll.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        poll.refresh_from_db()

        self.assertEqual(poll.title, payload['title'])

    def test_delete_poll(self):
        """Test delete poll success"""
        poll = Poll.objects.create(
            title='Profile poll',
            description='Get personal info',
            date_start='2020-05-15',
            date_end='2020-05-22',
            user=self.admin
        )

        url = detail_url(poll.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        exists = Poll.objects.filter(title=poll.title).exists()

        self.assertFalse(exists)


class PollUnableForSimpleUserTests(TestCase):
    """Tests question operations not allowed for simple user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'testuser', 'testpass'
        )
        self.client.force_authenticate(user=self.user)

    def test_user_connot_create_poll(self):
        """Test question create methos not allowed"""
        payload = {
            'title': 'Why not?',
            'description': 'I wont create it!',
            'date_start': '2020-05-15',
            'date_end': '2020-06-15',
            'user': self.user.id
        }

        res = self.client.post(POLL_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
