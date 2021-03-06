from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Question, Answer, Poll


def sample_user(username='username', password='password'):
    """Create sample user"""
    return get_user_model().objects.create_user(
        username=username, password=password
    )


class ModelsTests(TestCase):
    """Testing project's models"""

    def test_create_user_success(self):
        """Test create user with valid credentials"""
        username = 'testuser'
        password = 'testpass'
        user = get_user_model().objects.create_user(
            username=username, password=password
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_create_superuser(self):
        """Test is superuser created successfull"""
        superuser = get_user_model().objects.create_superuser(
            username='testsuperuser',
            password='testsuperpass',
            email='admin@company.com',
        )

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_question_success(self):
        """Test creating questions polls"""
        question = Question.objects.create(
            title='How old are you?', type='TEXT', user=sample_user()
        )

        self.assertEqual(str(question), question.title)

    def test_create_answer_success(self):
        """Test answer the question"""
        user = sample_user()
        user_id = 'Lm678tr'
        question = Question.objects.create(
            title='Whats up?', type='TEXT', user=user
        )

        answer = Answer.objects.create(
            content="I'm fine!", question=question, user_id=user_id
        )

        expected = f'{answer.question.id}-{answer.user_id}'
        self.assertEqual(str(answer), expected)

    def test_create_poll_success(self):
        """Test create poll"""
        user = sample_user()
        question = Question.objects.create(
            title='How are you?', type='TEXT', user=user
        )
        poll = Poll.objects.create(
            title='Profile poll',
            description='Get personal info',
            date_start='2020-05-15',
            date_end='2020-06-15',
            user=user,
        )
        poll.questions.add(question)

        self.assertEqual(str(poll), poll.title)
        self.assertEqual(poll.questions.count(), 1)
