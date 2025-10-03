from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WebhookView, TeamViewSet

router = DefaultRouter()
router.register(r'teams', TeamViewSet, basename="team")

urlpatterns = [
    path("webhook/", WebhookView.as_view(), name="webhook"),
    path("", include(router.urls)),   
]
