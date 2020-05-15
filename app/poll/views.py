from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from core.models import Question, Answer
from poll import serializers


class QuestionViewSet(viewsets.ModelViewSet):
    """Manage questions in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = serializers.QuestionSerializer
    queryset = Question.objects.all()

    def get_queryset(self):
        """Retrive all created question"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create new question"""
        serializer.save(user=self.request.user)


class AnswerViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """Viewset for answer questions"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Answer.objects.all()
    serializer_class = serializers.AnswerSerializer

    def get_queryset(self):
        """Return answer objects of current authentication user only"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create new answer"""
        serializer.save(user=self.request.user)
