from rest_framework.serializers import ModelSerializer
from comment.models import Comment
from rest_framework import serializers

class CommentSerializer(ModelSerializer):
    username=serializers.CharField(source="user.username",read_only=True)
    class Meta:
        model=Comment
        exclude=["created_at","updated_at"]