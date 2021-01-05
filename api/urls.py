from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('core/', include('core.urls', namespace="core")),
    path('api/', include('courses.urls', namespace="api")),
]
