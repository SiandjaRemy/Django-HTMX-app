from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count

from a_post.forms import CommentReplyCreateForm
from .models import Profile
from .forms import ProfileEditForm

# Create your views here.

User = get_user_model()

def profile_view(request, username=None):
    if username:
        profile = Profile.objects.filter(user__username=username).first()
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()
        
    posts = profile.user.posts.all()
    if request.htmx:
        if "top-posts" in request.GET:
            posts = profile.user.posts.annotate(number_of_likes=Count("likes")).filter(number_of_likes__gt=0).order_by("-number_of_likes")
            context = {
                "posts": posts
            }
            return render(request, "snippets/filterd_user_posts.html", context)
        elif "top-comments" in request.GET:
            comments = profile.user.comments.annotate(number_of_likes=Count("likes")).filter(number_of_likes__gt=0).order_by("-number_of_likes")
            comment_reply_form = CommentReplyCreateForm()
            if request.method == "POST":
                comment_reply_form = CommentReplyCreateForm(request.POST)
                
            context = {
                "comments": comments,
                "comment_reply_form": comment_reply_form,
            }
            return render(request, "snippets/filterd_user_comments.html", context)
        elif "liked-posts" in request.GET:
            # Think on how to order them by the date of creation of the like
            # posts = profile.user.liked_posts.all()
            posts = profile.user.liked_posts.order_by("-likedpost__created_at")
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