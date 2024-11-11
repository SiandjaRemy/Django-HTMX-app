
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    
    path("__debug__/", include("debug_toolbar.urls")),

    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),

    path("", include("a_post.urls")),
    path("profile/", include("a_users.urls")),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)