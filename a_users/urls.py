from django.urls import path
from .views import *


urlpatterns = [
    path("", profile_view, name="profile"),
    path("<str:username>", profile_view, name="user-profile"),
    path("edit/", profile_edit_view, name="profile-edit"),
    path("onboarding/", profile_edit_view, name="profile-onboarding"),
    path("delete/", profile_delete_view, name="profile-delete"),
    
]