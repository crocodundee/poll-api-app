from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Answer, Question
from poll.serializers import AnswerSerializer


ANSWER_URL = reverse('poll:answer-list')


class AnswerEndpointTests(TestCase):
    """Tests for answer on questions"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'testuser', 'testpass'
        )
        self.client.force_authenticate(user=self.user)
        self.question = Question.objects.create(
            title='How are you?',
            type='TEXT',
            user=self.user
        )

    def test_user_create_answer(self):
        """Test user answer"""
        payload = {
            'content': "I'm fine!",
            'question': self.question.id,
        }

        res = self.client.post(ANSWER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        answer = Answer.objects.get(content=payload['content'])
        serializer = AnswerSerializer(answer)
        self.assertEqual(res.data, serializer.data)
