# api/urls.py
from django.urls import path,include
from rest_framework import routers
from .views import GDViewSet

router = routers.DefaultRouter()
router.register('GD',GDViewSet)
urlpatterns = [
    path('', include(router.urls)),
]