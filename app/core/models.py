from django.db import models
from django.conf import settings


class Question(models.Model):
    """Polls question"""
    TEXT = 'TEXT'
    ONE_CHOICE = 'ONE_CHOICE'
    MULTIPLE_CHOICE = 'MULTIPLE_CHOICE'
    type_choices = [
        (TEXT, 'Text response'),
        (ONE_CHOICE, 'One choice response'),
        (MULTIPLE_CHOICE, 'Multiple choice response')
    ]

    title = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=255, choices=type_choices, default=TEXT)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Answer(models.Model):
    """User answers on questions"""
    content = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.question.id}-{self.user.username}'


class Poll(models.Model):
    """Poll for users interview"""
    title = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    date_start = models.DateField(auto_now_add=True, blank=False)
    date_end = models.DateField(auto_now=True, blank=True)
    questions = models.ManyToManyField('Question')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
