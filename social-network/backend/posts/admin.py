from django.contrib import admin

from .models import Post, LikesByDay


class PostAdmin(admin.ModelAdmin):
    fields = ('author_id', 'title', 'content', 'created_at', 'users_liked_ids')
    list_display = ('title', 'author_id', 'id')
    readonly_fields = ('created_at', 'users_liked_ids')


class LikesByDayAdmin(admin.ModelAdmin):
    fields = ('id', 'date', 'likes_count')
    list_display = ('date', 'likes_count', 'id')
    readonly_fields = ('date', 'likes_count', 'id')


admin.site.register(Post, PostAdmin)
admin.site.register(LikesByDay, LikesByDayAdmin)
