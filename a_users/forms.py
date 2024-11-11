from django import forms

from a_users.models import Profile

        
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user"]
        labels = {
            "realname" : "Name",
        }
        widgets = {
            "image" : forms.FileInput(),
            "bio" : forms.Textarea(attrs={"rows":3}),
        }
