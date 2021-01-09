from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, like_post, unlike_post, likes_analytics


router = DefaultRouter()
router.register(r'posts', PostViewSet, 'posts')


urlpatterns = [
    path('like-post/', like_post, name='like-post'),
    path('unlike-post/', unlike_post, name='unlike-post'),
    path('likes-analytics/', likes_analytics, name='likes-analytics'),
]

urlpatterns += router.urls
