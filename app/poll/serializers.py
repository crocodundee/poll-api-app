from rest_framework import serializers

from core.models import Question, Answer, Poll


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for pool's question"""

    class Meta:
        model = Question
        fields = ('id', 'title', 'type')
        read_only_fields = ('id',)


class AnswerSerializer(serializers.ModelSerializer):
    """Serializer for answer"""

    class Meta:
        model = Answer
        fields = ('id', 'content', 'question')
        read_only_fields = ('id',)


class AnswerDoneSerializer(serializers.ModelSerializer):
    """Serializer for answers to completed polls"""
    question = serializers.StringRelatedField()
    answer = serializers.CharField(source='content')

    class Meta:
        model = Answer
        fields = ('question', 'answer')


class PollDetailSerializer(serializers.ModelSerializer):
    """Poll serializer"""
    questions = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Question.objects.all()
    )

    class Meta:
        model = Poll
        fields = (
            'id', 'title', 'description',
            'date_start', 'date_end', 'questions'
        )
        read_only_fields = ('id', 'date_start',)


class PollSerializer(serializers.ModelSerializer):
    """Short poll serializer"""

    class Meta:
        model = Poll
        fields = ('id', 'title')


class PollDoneSerializer(serializers.Serializer):
    """Serializer for polls compited by user"""
    poll = PollSerializer()
    answers = AnswerDoneSerializer(many=True)
