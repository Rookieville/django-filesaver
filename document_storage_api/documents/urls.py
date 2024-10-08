from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import DocumentViewSet

router = DefaultRouter()
router.register(r'documents', DocumentViewSet)

urlpatterns = router.urls