from django.urls import path
from .views import *


urlpatterns = [
    path("", home_view, name="home"),
    path("category/<str:tag>/", home_view, name="category"),

    path("post/create/", post_create_view, name="post-create"),
    path("post/delete/<uuid:pk>/", post_delete_view, name="post-delete"),
    path("post/edit/<uuid:pk>/", post_edit_view, name="post-edit"),
    path("post/<uuid:pk>/", post_detail_view, name="post-detail"),
    path("post/<uuid:pk>/like/", like_post_view, name="like-post"),
    path("comment-sent/<uuid:pk>/", comment_sent_view, name="comment-sent"),
    path("comment/like/<uuid:pk>/", like_comment_view, name="like-comment"),
    path("comment-delete/<uuid:pk>/", comment_delete_view, name="comment-delete"),
    path("comment-reply-sent/<uuid:pk>/", comment_reply_sent_view, name="comment-reply-sent"),
    path("comment-reply/like/<uuid:pk>/", like_comment_reply_view, name="like-comment-reply"),
    path("comment-reply-delete/<uuid:pk>/", comment_reply_delete_view, name="comment-reply-delete"),
]