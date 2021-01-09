from django.utils.datetime_safe import date
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.validators import ValidationError

from .serializers import PostCreationSerializer, PostListSerializer, LikesCountByDaySerializer, PostRetrieveSerializer
from ..models import Post, LikesByDay


class PostViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin, CreateModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = PostCreationSerializer(data=data)
        if serializer.is_valid():
            serializer.save(author_id=request.jwt_user['user_id'])
            return Response(serializer.data, status=201)
        return Response({'error': serializer.errors})

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostRetrieveSerializer
        return super(PostViewSet, self).retrieve(request, *args, **kwargs)


@api_view(['POST'])
def like_post(request):
    data = request.data
    user_id = request.jwt_user.get('user_id')
    if 'post_id' not in data:
        raise ValidationError({'post_id': 'this field is required'})
    if type(data.get('post_id')) != int:
        raise ValidationError({'post_id': 'this field must be integer'})
    try:
        post = Post.objects.get(id=data.get('post_id'))
        if user_id not in post.users_liked_ids:
            post.like(user_id)
            post.save()
            return Response({'success': 'Post has been successfully liked'}, status=200)
        return Response({'error': 'The user has already liked this post'}, status=403)
    except Post.DoesNotExist:
        return Response({'post_id': 'No post with this id'}, status=404)


@api_view(['POST'])
def unlike_post(request):
    data = request.data
    user_id = request.jwt_user.get('user_id')
    if 'post_id' not in data:
        raise ValidationError({'post_id': 'this field is required'})
    if type(data.get('post_id')) != int:
        raise ValidationError({'post_id': 'this field must be integer'})
    try:
        post = Post.objects.get(id=data.get('post_id'))
        if user_id in post.users_liked_ids:
            post.unlike(user_id)
            post.save()
            return Response({'success': 'Post has been successfully unliked'}, status=200)
        return Response({'error': 'The user has not liked this post yet'}, status=403)
    except Post.DoesNotExist:
        return Response({'post_id': 'No post with this id'}, status=404)


@api_view(['GET'])
def likes_analytics(request, *args, **kwargs):
    query_params = request.query_params
    if 'date_from' not in query_params:
        raise ValidationError({'date_from': 'This parameter is required'})
    if 'date_to' not in query_params:
        raise ValidationError({'date_to': 'This parameter is required'})
    date_from = date.fromisoformat(query_params.get('date_from'))
    date_to = date.fromisoformat(query_params.get('date_to'))

    likes = LikesByDay.objects.filter(date__gte=date_from, date__lte=date_to)
    serializer = LikesCountByDaySerializer(likes, many=True)
    return Response({'dates': serializer.data}, status=200)


