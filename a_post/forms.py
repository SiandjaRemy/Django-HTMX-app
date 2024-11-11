from django import forms

from a_post.models import Comment, CommentReply, Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["url", "body", "tags"]
        # fields = "__all__"
        labels = {
            "body" : "caption",
            "tags" : "category",
        }
        widgets = {
            "body" : forms.Textarea(attrs={"rows": 3, "placeholder": "Add a caption ...", "class": "font1 text-4xl"}),
            "url" : forms.TextInput(attrs={"placeholder": "Add url ..."}),
            "tags" : forms.CheckboxSelectMultiple(),
        }
        
class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["body", "tags"]
        labels = {
            "body" : "",
            "tags" : "category",
        }
        widgets = {
            "body" : forms.Textarea(attrs={"rows": 3, "class": "font1 text-4xl"}),
            "tags" : forms.CheckboxSelectMultiple(),
        }


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        labels = {
            "body" : "",
        }
        widgets = {
            "body" : forms.TextInput(attrs={"placeholder": "Add comment now..."}),
        }
        
class CommentReplyCreateForm(forms.ModelForm):
    class Meta:
        model = CommentReply
        fields = ["body"]
        labels = {
            "body" : "",
        }
        widgets = {
            "body" : forms.TextInput(attrs={"placeholder": "Add reply..."}),
        }
