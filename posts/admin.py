from django.contrib import admin
from .models import Post, Comment, Like, Tag, PostImage

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    #exclude = ("is_deleted",)
    #fields = ("text", ("user", status), "tags")
    fieldsets =(
        ('details', {
            'fields': ('text', ("user", status), "tags"),
        }),
    )

admin.site.register(PostImage)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Tag)

