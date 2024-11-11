from django.db import models
from django.contrib.auth import get_user_model
from django.templatetags.static import static
import uuid

# Create your models here.

User = get_user_model()


class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to='avatars/', blank=True, null=True)
    realname = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.user)
    
    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static("images/avatar_default.svg")
        return avatar
    
    @property
    def name(self):
        try:
            name = self.realname
        except:
            name = self.user.username
        return name
