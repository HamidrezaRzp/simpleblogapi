from rest_framework import serializers
from .models import Post
from django.contrib.auth import get_user_model


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'title',
            'author',
            'body',
            'created_at',
        )
        model = Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'username',
        )
        model = get_user_model()