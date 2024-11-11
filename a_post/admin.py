from django.contrib import admin
from .models import Comment, CommentReply, LikedComment, LikedPost, LikedReply, Post, Tag
# Register your models here.


class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author"]


admin.site.register(Post, PostAdmin)
admin.site.register(LikedPost)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment)
admin.site.register(LikedComment)
admin.site.register(CommentReply)
admin.site.register(LikedReply)
