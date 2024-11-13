from django.template import Library, library
from django.contrib.auth import get_user_model
from django.db.models import Count, Prefetch

from a_post.models import Tag, Post, Comment

User = get_user_model()

register = Library()


@register.inclusion_tag("includes/sidebar.html")
def sidebar_view(tag=None, user=None):
    all_categories = Tag.objects.all()
    top_post = (
        Post.objects.annotate(
            number_of_likes=Count("likes"),
        )
        .select_related("author")
        .prefetch_related("likes", "comments", "author__profile")
        .filter(number_of_likes__gt=0)
        .order_by("-number_of_likes")
    )
    top_comments = (
        Comment.objects.annotate(
            number_of_likes=Count("likes"),
        )
        .select_related("author", "parent_post")
        .prefetch_related("likes", "replies", "author__profile")
        .filter(number_of_likes__gt=0)
        .order_by("-number_of_likes")
    )

    # if user:
    #     user = User.objects.prefetch_related("profile", "liked_posts", "liked_comments").filter(username=user.username)

    context = {
        "categories": all_categories,
        "top_post": top_post,
        "top_comments": top_comments,
        "tag": tag,
        "user": user,
    }
    return context
