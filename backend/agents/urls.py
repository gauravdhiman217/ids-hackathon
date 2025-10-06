from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WebhookView, AgentViewSet, TypeViewSet, ServiceViewSet, TicketPriorityViewSet


router = DefaultRouter()
router.register(r'agents', AgentViewSet, basename="Agent")



urlpatterns = [
    path("webhook/", WebhookView.as_view(), name="webhook"),
    path("", include(router.urls)),   
    path("types/", TypeViewSet.as_view()),
    path("services/", ServiceViewSet.as_view()),
    path("ticket-priorities/", TicketPriorityViewSet.as_view()),

]
