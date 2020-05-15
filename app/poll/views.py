from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from core.models import Question
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
