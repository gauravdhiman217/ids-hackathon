from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import process_ticket_data
from rest_framework import viewsets, generics

from .models import Agent
from .serializers import AgentSerializer, AgentSkillSerializer, TypeSerializer, ServiceSerializer, TicketPrioritySerializer
from .models import Agent, Type, Service, TicketPriority
from core.base import BaseModelViewSet,BaseRetrieveListView



class WebhookView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        ticket_id = data.get("TicketID")
        if ticket_id:
            process_ticket_data.delay(ticket_id)
        return Response({"status": "success"}, status=200)




class AgentViewSet(BaseModelViewSet):
    queryset = Agent.objects.all().order_by("agent_id")
    serializer_class = AgentSerializer
    pagination_class = None

    def create(self, request, *args, **kwargs):
        return Response(
            {
                "status": False,
                "status_code": 400,
                "message": "Method not allowed",

            }
        )


class TypeViewSet(BaseRetrieveListView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    pagination_class = None

class ServiceViewSet(BaseRetrieveListView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    pagination_class = None


class TicketPriorityViewSet(BaseRetrieveListView):
    queryset = TicketPriority.objects.all()
    serializer_class = TicketPrioritySerializer
    pagination_class = None


class AgentSkillView(BaseRetrieveListView):
    queryset = Agent.objects.filter(is_valid=True, role__isnull=False).distinct("role")
    serializer_class = AgentSkillSerializer
    pagination_class = None