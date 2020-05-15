from rest_framework import serializers

from core.models import Question, Answer


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
