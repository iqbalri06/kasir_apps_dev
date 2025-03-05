from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Make sure you have this line
    path('members/', include('members.urls', namespace='members')),
    # Other URLs
]
