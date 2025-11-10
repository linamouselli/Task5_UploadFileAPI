from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UploadViewSet

router = DefaultRouter()
router.register(r'uploads', UploadViewSet, basename='uploads')
urlpatterns = [
    path('api/', include(router.urls)),
]