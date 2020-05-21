from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Answer, Question, Poll
from poll.serializers import AnswerSerializer


def answer_url(user_id, poll_id, q_id):
    """Create url for answer poll's question"""
    return reverse('poll:poll-complete', args=[user_id, poll_id, q_id])


class AnswerEndpointTests(TestCase):
    """Tests for answer on questions"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'testuser', 'testpass'
        )
        self.user_id = '123'
        self.client.force_authenticate(user=self.user)
        self.question = Question.objects.create(
            title='How are you?', type='TEXT', user=self.user
        )
        self.poll = Poll.objects.create(
            title='Simple poll',
            description='New simple poll',
            date_start='2020-05-21',
            date_end='2020-06-21',
            user=self.user,
        )
        self.poll.questions.add(self.question)

    def test_user_create_answer(self):
        """Test user answer"""
        payload = {'content': "I'm fine!"}
        url = answer_url(self.user_id, self.poll.id, self.question.id)
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        answer = Answer.objects.get(
            user_id=self.user_id, question__id=self.question.id
        )
        serializer = AnswerSerializer(answer)
        self.assertEqual(res.data, serializer.data)

        res = self.client.post(url, payload)
        seld.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        url = answer_url(self.user_id, self.poll.id, self.question.id + 1)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
