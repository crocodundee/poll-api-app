from collections import namedtuple

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
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

    def get_permissions(self):
        """Set permissions for actions"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [
                IsAuthenticated,
            ]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Retrive all created objects"""
        if self.action in ['list', 'retrieve']:
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create new object"""
        serializer.save(user=self.request.user)


class QuestionViewSet(AdminManageViewSet):
    """Manage questions in the database"""

    serializer_class = serializers.QuestionSerializer
    queryset = Question.objects.all()


class PollViewSet(AdminManageViewSet):
    """Viewset for manage poll"""

    queryset = Poll.objects.all()
    serializer_class = serializers.PollDetailSerializer

    def get_serializer_class(self):
        """Set serializer for action in poll endpoint"""
        if self.action in ['list', 'retrive']:
            return serializers.PollDetailSerializer
        elif self.action == 'add_question':
            return serializers.QuestionSerializer
        elif self.action == 'complete':
            return serializers.AnswerSerializer
        return serializers.PollCrudSerializer

    @action(methods=['POST', 'PUT', 'PATCH'], detail=True, name='Add question')
    def add_question(self, request, pk=None):
        """Add question to poll"""
        poll = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            question = Question.objects.get(
                title=serializer.validated_data.get('title')
            )
            poll.questions.add(question)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET', 'POST'], detail=True, name='Complete the poll')
    def complete(self, request, user_id=None, pk=None, question_id=None):
        """
        Complete poll by user

        get:
        View question details

        post:
        Answer the question
        """
        poll = self.get_object()
        polls_questions = (q.id for q in poll.questions.all())
        answer_exists = Answer.objects.filter(
            user_id=user_id, question__id=question_id
        ).exists()

        if question_id not in polls_questions:
            error_msg = 'Question not allowed'
        elif answer_exists:
            error_msg = 'You have alredy answered this question'
        else:
            question = Question.objects.get(id=question_id)

            if request.method == 'GET':
                serializer = serializers.QuestionSerializer(question)
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                serializer = self.get_serializer(data=request.data)

                if serializer.is_valid():
                    serializer.save(question=question, user_id=user_id)
                    return Response(serializer.data, status.HTTP_201_CREATED)
                error_msg = serializer.errors
        return Response({'error': error_msg}, status.HTTP_400_BAD_REQUEST)


class PollDoneViewSet(viewsets.ViewSet):
    """Viewset to list polls completed by current user"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        """Return all completed polls by user"""
        user_id = self.request.query_params.get('user')
        answers = Answer.objects.filter(user_id=user_id)
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

        return Response({'info': 'You have not complete any poll'})
