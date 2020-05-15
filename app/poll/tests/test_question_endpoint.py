from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Question
from poll.serializers import QuestionSerializer


QUESTION_URL = reverse('poll:question-list')


def detail_url(q_id):
    """Get question detail url"""
    return reverse('poll:question-detail', args=[q_id])


class QuestionEndpointCRUDTests(TestCase):
    """Test Question endpoint CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            username='admin',
            password='adminpass',
            email='admin@company.com'
        )
        self.client.force_authenticate(user=self.admin)

    def test_create_question(self):
        """Test admin can create question"""
        payload = {
            'title': 'How are you?',
            'type': 'TEXT'
        }
        res = self.client.post(QUESTION_URL, payload)

        self.assertEqual(res.status_code, status. HTTP_201_CREATED)

        q = Question.objects.get(title=payload['title'])
        serializer = QuestionSerializer(q)

        self.assertEqual(res.data, serializer.data)

    def test_update_question(self):
        """Test admin can update question"""
        q = Question.objects.create(
            title='Simple question',
            type='TEXT',
            user=self.admin
        )

        payload = {
            'title': 'Updated question',
            'type': 'ONE_CHOICE'
        }

        url = detail_url(q.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_question(self):
        """Test delete question success"""
        q = Question.objects.create(
            title='Why???',
            type='ONE_CHOICE',
            user=self.admin
        )

        url = detail_url(q.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        exists = Question.objects.filter(title=q.title).exists()

        self.assertFalse(exists)


class QuestionUnableForSimpleUserTests(TestCase):
    """Tests question operations not allowed for simple user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'testuser', 'testpass'
        )
        self.client.force_authenticate(user=self.user)

    def test_user_connot_create_question(self):
        """Test question create methos not allowed"""
        payload = {
            'title': 'Why not?',
            'type': 'TEXT'
        }

        res = self.client.post(QUESTION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
