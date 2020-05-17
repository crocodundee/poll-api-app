from collections import namedtuple

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from core.models import Question, Answer, Poll
from poll import serializers


PollsDone = namedtuple('PollsDone', ('poll', 'answers'))


class AdminManageViewSet(viewsets.ModelViewSet):
    """Admin operations viewset"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_queryset(self):
        """Retrive all created objects"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create new object"""
        serializer.save(user=self.request.user)


class QuestionViewSet(AdminManageViewSet):
    """Manage questions in the database"""
    serializer_class = serializers.QuestionSerializer
    queryset = Question.objects.all()


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


class PollViewSet(AdminManageViewSet):
    """Viewset for manage poll"""
    queryset = Poll.objects.all()
    serializer_class = serializers.PollDetailSerializer


class PollDoneViewSet(viewsets.ViewSet):
    """Viewset to list polls completed by current user"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        """Return answer objects of current authentication user only"""
        answers = Answer.objects.filter(user=self.request.user)
        result = []

        if answers:
            polls = Poll.objects.all()

            for poll in polls:
                questions = [q.id for q in poll.questions.all()]
                response = answers.filter(question__id__in=questions)
                if response:
                    result.append(PollsDone(poll, response))

            serializer = serializers.PollDoneSerializer(result, many=True)

            return Response(serializer.data)

        return Response({'error': 'You have not complete any poll'})
