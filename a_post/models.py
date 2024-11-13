from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.utils.text import slugify

# Create your models here.

User = get_user_model()

class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    author = models.ForeignKey(User, related_name="posts", null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    image = models.URLField(max_length=500)
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name="liked_posts", through="LikedPost")
    tags = models.ManyToManyField("Tag", related_name="posts")
    artist = models.CharField(max_length=500, null=True)
    url = models.URLField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        string = self.title
        return str(string)
    
    
    class Meta:
        ordering = ["-modified_at"]
        

class LikedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
        

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"
    

class Tag(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, *kwargs)
        
    class Meta:
        ordering = ["-created_at"]


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    author = models.ForeignKey(User, related_name="comments", null=True, blank=True, on_delete=models.SET_NULL)
    parent_post = models.ForeignKey(Post, related_name="comments", null=True, blank=True, on_delete=models.CASCADE)
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User, related_name="liked_comments", through="LikedComment")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        try:
            return f"{self.author.username} : {self.body[:30]}"
        except:
            return f"No author : {self.body[:30]}"

    class Meta:
        ordering = ["-created_at"]



class LikedComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return f"{self.user.username} liked {self.comment.body[:30]}"
    
    

class CommentReply(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    author = models.ForeignKey(User, related_name="replies", null=True, blank=True, on_delete=models.SET_NULL)
    parent_comment = models.ForeignKey(Comment, related_name="replies", null=True, blank=True, on_delete=models.CASCADE)
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User, related_name="liked_replies", through="LikedReply")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        try:
            return f"{self.author.username} : {self.body[:30]}"
        except:
            return f"No author : {self.body[:30]}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Comment Replies"


class LikedReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey(CommentReply, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return f"{self.user.username} liked {self.reply.body[:30]}"

    class Meta:
        verbose_name_plural = "Liked Replies"
