from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework.routers import DefaultRouter

from accounts.api.urls import urlpatterns as accounts_urls


api_patterns = [
    path('', include(accounts_urls))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include((api_patterns, 'api'), namespace='api'))
]
urlpatterns += staticfiles_urlpatterns()
