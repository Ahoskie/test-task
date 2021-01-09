from django.utils.timezone import now
from django.db import models
from django.contrib.postgres.fields.array import ArrayField


class Post(models.Model):
    author_id = models.PositiveIntegerField()
    title = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    users_liked_ids = ArrayField(
        base_field=models.PositiveIntegerField(),
        blank=True,
        default=list
    )

    def like(self, user_id):
        if user_id not in self.users_liked_ids:
            self.users_liked_ids.append(user_id)
            likes_by_day, created = LikesByDay.objects.get_or_create(date=now())
            likes_by_day.likes_count += 1
            likes_by_day.save()

    def unlike(self, user_id):
        if user_id in self.users_liked_ids:
            self.users_liked_ids.remove(user_id)
            likes_by_day, created = LikesByDay.objects.get_or_create(date=now())
            likes_by_day.likes_count -= 1
            likes_by_day.save()


class LikesByDay(models.Model):
    date = models.DateField()
    likes_count = models.IntegerField(default=0)
