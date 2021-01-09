from django.apps import AppConfig


class PostsConfig(AppConfig):
    name = 'posts'

    def ready(self):
        from posts.models import LikesByDay
        from django.utils.timezone import now
        LikesByDay.objects.get_or_create(date=now())
