from rest_framework import serializers

from core.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for pool's question"""

    class Meta:
        model = Question
        fields = ('id', 'title', 'type')
        read_only_fields = ('id',)
