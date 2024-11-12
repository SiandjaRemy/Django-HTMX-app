from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count

from a_post.forms import CommentReplyCreateForm
from a_post.models import Post, Comment
from .models import Profile
from .forms import ProfileEditForm

# Create your views here.

User = get_user_model()

def profile_view(request, username=None):
    if username:
        profile = Profile.objects.prefetch_related("user").filter(user__username=username).first()
    else:
        try:
            profile = Profile.objects.select_related("user").prefetch_related("user").filter(user=request.user).first()
        except:
            raise Http404()
        
    posts = Post.objects.annotate(number_of_likes=Count("likes"), number_of_comments=Count("comments")).select_related("author").prefetch_related("tags", "likes", "author__profile__user").filter(author=profile.user)
    if request.htmx:
        if "top-posts" in request.GET:
            posts = Post.objects.annotate(number_of_likes=Count("likes"), number_of_comments=Count("comments")).select_related("author").prefetch_related("tags", "likes", "author__profile__user").filter(author=profile.user).filter(number_of_likes__gt=0).order_by("-number_of_likes")
            context = {
                "posts": posts
            }
            return render(request, "snippets/filterd_user_posts.html", context)
        elif "top-comments" in request.GET:
            comments = Comment.objects.annotate(number_of_likes=Count("likes"), number_of_replies=Count("replies")).select_related("author", "parent_post").prefetch_related("likes", "replies").filter(author=profile.user, number_of_likes__gt=0).order_by("-number_of_likes")
            comment_reply_form = CommentReplyCreateForm()
            if request.method == "POST":
                comment_reply_form = CommentReplyCreateForm(request.POST)
                
            context = {
                "comments": comments,
                "comment_reply_form": comment_reply_form,
            }
            return render(request, "snippets/filterd_user_comments.html", context)
        elif "liked-posts" in request.GET:
            posts = Post.objects.annotate(number_of_likes=Count("likes"), number_of_comments=Count("comments")).select_related("author").prefetch_related("tags", "likes", "comments", "author__profile").filter(author=profile.user).order_by("-likedpost__created_at")
            context = {
                "posts": posts
            }
            return render(request, "snippets/filterd_user_posts.html", context)
        else:
            context = {
                "posts": posts
            }
            return render(request, "snippets/filterd_user_posts.html", context)
            
    context = {
        "profile": profile,
        "posts": posts,
    }
    return render(request, "a_users/profile.html", context)


@login_required
def profile_edit_view(request):
    profile = request.user.profile
    form = ProfileEditForm(instance=profile)
    
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            
            return redirect("profile")
        
    if request.path == reverse("profile-onboarding"):
        template = "a_users/profile_onboarding.html"
    else:
        template = "a_users/profile_edit.html"
            
    context = {
        "profile": profile,
        "form": form,
    }
    return render(request, template, context)


@login_required
def profile_delete_view(request):
    user = request.user
    
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, "Account deleted. What a pity")
        return redirect("/")
            
    return render(request, "a_users/profile_delete.html")