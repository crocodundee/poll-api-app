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


class PollSerializer(serializers.ModelSerializer):
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
