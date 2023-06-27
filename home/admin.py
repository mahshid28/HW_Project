from django.contrib import admin
from posts.models import Post, Comment, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('user', 'slug', 'updated_at')
	search_fields = ('slug', 'content')
	list_filter = ('updated_at',)
	prepopulated_fields = {'slug':('content',)}
	raw_id_fields = ('user',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('user', 'related_post', 'created_at', 'is_reply')
	raw_id_fields = ('user', 'related_post', 'reply_to')


admin.site.register(Like)