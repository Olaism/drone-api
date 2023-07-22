from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include("drones.urls",namespace='v1')),
    path("v1/api-auth/", include("rest_framework.urls")),
    path('v2/', include("drones.v2.urls",namespace='v2')),
    path('v2/api-auth/', include('rest_framework.urls')),
]
