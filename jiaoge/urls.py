"""jiaoge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from postcards.urls import doc_paths, router
from .views import landing


urlpatterns = [
    # Hide the Admin panel a bit.
    path(settings.ADMIN_URL, admin.site.urls),
    # Landing/start page.
    path(r'', landing, name='landing'),

    # POSTCARD VIEWS #
    # Classic HTML-based views.
    path(r'', include(doc_paths)),
    # JSON API views.
    path(r'api/', include(router.urls)),
    path(r'api-auth/',
         include('rest_framework.urls', namespace='rest_framework')),
]
