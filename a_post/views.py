from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages
from django.core.paginator import Paginator

from a_post.models import Comment, CommentReply, Post, Tag
from a_post.forms import CommentCreateForm, CommentReplyCreateForm, PostCreateForm, PostEditForm

from bs4 import BeautifulSoup
import requests


# Create your views here.

def home_view(request, tag=None):

    if tag is not None:
        try:
            all_posts = Post.objects.annotate(number_of_likes=Count("likes"), number_of_comments=Count("comments")).select_related("author").prefetch_related("tags", "likes", "comments").filter(tags__slug=tag).order_by("-created_at")
            tag = Tag.objects.filter(slug=tag).first()
        except Exception as e:
            print(f"Error: {e}")
    else:
        all_posts = Post.objects.annotate(number_of_likes=Count("likes"), number_of_comments=Count("comments")).select_related("author").prefetch_related("tags", "likes", "comments", "author__profile").all().order_by("-created_at")
    
    paginator = Paginator(all_posts, 3)
    page = int(request.GET.get("page", 1))
    try:
        posts = paginator.page(page)
    except:
        return HttpResponse("")
    
    context = {
        "posts": posts,
        "tag": tag,
        "page": page,
    }
    
    if request.htmx:
        return render(request, "snippets/home_posts_paginator.html", context)
    
    return render(request, "a_post/home.html", context)


@login_required
def post_create_view(request):
    form = PostCreateForm()
    context = {
        "form": form
    }
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            
            try:
                website = requests.get(form.data["url"])
            
                source_code = BeautifulSoup(website.text, "html.parser")
                
                find_image = source_code.select('meta[content^="https://live.staticflickr.com/"]')
                image = find_image[0]["content"]
                post.image = image
                
                find_title = source_code.select('h1.photo-title')
                title = find_title[0].text.strip()
                post.title = title
                
                
                find_artist = source_code.select('a.owner-name')
                artist = find_artist[0].text.strip()
                post.artist = artist
                
                post.author = request.user
                
                
                post.save()
                form.save_m2m()
                return redirect("home")
            except Exception as e:
                messages.error(request, "Something went wrong")
                print(f"Error: {e}")
                # return redirect("post-create")
        
    return render(request, "a_post/post_create.html", context)


@login_required
def post_delete_view(request, pk):
    try:
        post = Post.objects.filter(id=pk, author=request.user).first()
    except:
        raise Http404()
    
    context = {
        "post": post
    }
    
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted")
        return redirect("home")
        
    return render(request, "a_post/post_delete.html", context)


@login_required
def post_edit_view(request, pk):
    post = Post.objects.filter(id=pk, author=request.user).first()
    form = PostEditForm(instance=post)
    
    if request.method == "POST":
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated")
            return redirect("home")

    context = {
        "post": post,
        "form": form,
    }
    
    return render(request, "a_post/post_edit.html", context)


def post_detail_view(request, pk):
    try:
        post = Post.objects.annotate(number_of_likes=Count("likes"), number_of_comments=Count("comments")).select_related("author").prefetch_related("tags", "likes", "comments").filter(id=pk).first()
        comment_form = CommentCreateForm()
        comment_reply_form = CommentReplyCreateForm()
    except:
        raise Http404()
    

    if request.htmx:
        if "top" in request.GET:
            # comments = post.comments.annotate(number_of_likes=Count("likes")).filter(number_of_likes__gt=0).order_by("-number_of_likes")
            comments = Comment.objects.annotate(number_of_likes=Count("likes"), number_of_replies=Count("replies")).select_related("author", "parent_post").prefetch_related("likes", "replies", "author__profile").filter(parent_post=post, number_of_likes__gt=0).order_by("-number_of_likes")
        else:
            # comments = post.comments.annotate(number_of_likes=Count("likes")).comments.all()
            comments = Comment.objects.annotate(number_of_likes=Count("likes"), number_of_replies=Count("replies")).select_related("author", "parent_post").prefetch_related("likes", "replies", "author__profile").filter(parent_post=post)
        context = {
            "comments": comments,
            "comment_reply_form": comment_reply_form,
        }
        return render(request, "snippets/filtered_comments.html", context)
        

    context = {
        "post": post,
        "comment_form": comment_form,
        "comment_reply_form": comment_reply_form,
    }
    return render(request, "a_post/post_detail.html", context)


@login_required
def comment_sent_view(request, pk):
    post = Post.objects.filter(id=pk).first()
    comment_reply_form = CommentReplyCreateForm()
    
    if request.method == "POST":
        comment_form = CommentCreateForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()
            
    context = {
        "comment": comment,
        "post": post,
        "comment_reply_form": comment_reply_form,
    }
    print(f"Context: {context}")
    return render(request, "snippets/add_comment.html", context)
        

@login_required
def comment_delete_view(request, pk):
    try:
        comment = Comment.objects.filter(id=pk, author=request.user).first()
        if comment is not None:  # Check if the comment object exists
            parent_post_id = comment.parent_post.id
            comment.delete()
            messages.success(request, "Comment deleted")
            return redirect("post-detail", parent_post_id)
        else:
            messages.error(request, "Comment not found or you do not have permission to delete it.")
            return redirect("post-detail", pk)  # Redirect to a suitable page or URL in case the comment is not found or user does not have permission

    except Comment.DoesNotExist:
        raise Http404()
        


@login_required
def comment_reply_sent_view(request, pk):
    comment = Comment.objects.filter(id=pk).first()
    
    if request.method == "POST":
        comment_reply_form = CommentReplyCreateForm(request.POST)
        if comment_reply_form.is_valid():
            comment_reply = comment_reply_form.save(commit=False)
            comment_reply.author = request.user
            comment_reply.parent_comment = comment
            comment_reply.save()
            
    context = {
        "reply": comment_reply,
        "comment": comment,
    }
    print(f"Context: {context}")
    return render(request, "snippets/add_comment_reply.html", context)
    
    

@login_required
def comment_reply_delete_view(request, pk):
    try:
        comment_reply = CommentReply.objects.filter(id=pk, author=request.user).first()
        if comment_reply is not None:  # Check if the comment object exists
            post_id = comment_reply.parent_comment.parent_post.id
            comment_reply.delete()
            messages.success(request, "Reply deleted")
            return redirect("post-detail", post_id)
        else:
            messages.error(request, "Comment reply not found or you do not have permission to delete it.")
            return redirect("post-detail", pk)  # Redirect to a suitable page or URL in case the comment is not found or user does not have permission

    except CommentReply.DoesNotExist:
        raise Http404()
        
        
        
def like_toggle(model):
    def inner_function(func):
        def wrapper(request, *args, **kwargs):
            pk = kwargs.get("pk")
            object = model.objects.filter(id=pk).first()
            already_liked = object.likes.filter(username=request.user.username).exists()
            if object is not None and object.author != request.user:
                if already_liked:
                    object.likes.remove(request.user)
                else:
                    object.likes.add(request.user)
            else:
                messages.error(request, "You cant like your own object")
            return func(request, object)
        return wrapper
    return inner_function



@login_required
@like_toggle(Post)
def like_post_view(request, object):
    context = {
        "post": object,
    }
    return render(request, "snippets/post_likes.html", context)


@login_required
@like_toggle(Comment)
def like_comment_view(request, object):
    context = {
        "comment": object,
    }
    return render(request, "snippets/comment_likes.html", context)


@login_required
@like_toggle(CommentReply)
def like_comment_reply_view(request, object):
    context = {
        "reply": object,
    }
    return render(request, "snippets/comment_reply_likes.html", context)

