from rest_framework import serializers
from .models import Post, Hashtag


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ["name"]


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "image")


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "user", "title"]


class PostDetailsSerializer(PostSerializer):
    hashtags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = ["id", "user", "title", "content", "image",
                  "created_at", "updated_at", "hashtags"]
