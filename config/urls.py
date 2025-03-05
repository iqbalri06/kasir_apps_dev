from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Update this line to include simple_shop URLs correctly
    path('', include('simple_shop.urls')),  # Remove any prefix to make URLs work from root
]

# Move static URLs to the end
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
