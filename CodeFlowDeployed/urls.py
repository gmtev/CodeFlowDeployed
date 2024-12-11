
# from django.conf import settings
# from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('CodeFlowDeployed.common.urls')),

    path('accounts/', include('CodeFlowDeployed.accounts.urls')),
    path('content/', include('CodeFlowDeployed.content.urls')),
]

# if settings.DEBUG:  no longer needed since cloudinary is used for media files
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
