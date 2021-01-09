from rest_framework import serializers
from rest_framework.validators import ValidationError

from ..models import Post, LikesByDay
from posts.services.rest_client.rest_client import get_users_info


class PostCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content'
        ]

    def create(self, validated_data, *args, **kwargs):
        title = validated_data.get('title')
        content = validated_data.get('content')
        author_id = validated_data.get('author_id')
        if not author_id:
            raise ValidationError({'error': 'Author id is not defined'})
        post = Post.objects.create(title=title, content=content, author_id=author_id)
        return post


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(method_name='get_author_username')
    users_liked = serializers.SerializerMethodField(method_name='get_users_liked')

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'author',
            'users_liked'
        ]

    def get_author_username(self, instance: Post):
        user_info = get_users_info([instance.author_id])
        username = 'AnonymousUser'
        if user_info:
            username = user_info[len(user_info)-1]['username']
        return username

    def get_users_liked(self, instance: Post):
        users_info = get_users_info(instance.users_liked_ids[:3])
        return [user_info['username'] for user_info in users_info]


class PostRetrieveSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(method_name='get_author_username')
    users_liked = serializers.SerializerMethodField(method_name='get_users_liked')

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'author',
            'users_liked'
        ]

    def get_author_username(self, instance: Post):
        user_info = get_users_info([instance.author_id])
        username = 'AnonymousUser'
        if user_info:
            username = user_info[len(user_info) - 1]['username']
        return username

    def get_users_liked(self, instance: Post):
        users_info = get_users_info(instance.users_liked_ids)
        return [user_info['username'] for user_info in users_info]


class LikesCountByDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = LikesByDay
        fields = '__all__'
