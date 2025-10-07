from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import process_ticket_data
from rest_framework import viewsets, generics

from .models import Agent
from .serializers import AgentSerializer, AgentSkillSerializer, TypeSerializer, ServiceSerializer, TicketPrioritySerializer
from .models import Agent, Type, Service, TicketPriority, TicketLog
from core.base import BaseModelViewSet,BaseRetrieveListView
from django.db.models import Count
from datetime import datetime


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

    def get_queryset(self):
        top_service_ids = (
            TicketLog.objects.filter(service__isnull=False)
            .values('service__service_id')
            .annotate(ticket_count=Count('ticket_id', distinct=True))
            .order_by('-ticket_count')[:5]
            .values_list('service__service_id', flat=True)
        )
        return Service.objects.filter(service_id__in=top_service_ids)


class TicketPriorityViewSet(BaseRetrieveListView):
    queryset = TicketPriority.objects.all()
    serializer_class = TicketPrioritySerializer
    pagination_class = None


class AgentSkillView(BaseRetrieveListView):
    queryset = Agent.objects.filter(is_valid=True, role__isnull=False).distinct("role")
    serializer_class = AgentSkillSerializer
    pagination_class = None


class DashboardView(APIView):
    def get(self, request, *args, **kwargs):
        today = datetime.now().date()

        total_users = Agent.objects.filter(is_valid=True).count()
        total_tickets = TicketLog.objects.values('ticket_id').distinct().count()

        tasks_today = TicketLog.objects.filter(
            created_at__date=today
        ).values('ticket_id').distinct().count()

        top_services = (
            TicketLog.objects.filter(service__isnull=False)
            .values('service__service_name')
            .annotate(ticket_count=Count('ticket_id', distinct=True))
            .order_by('-ticket_count')[:5]
        )
        top_5_services = [
            {"service_name": s["service__service_name"], "ticket_count": s["ticket_count"]}
            for s in top_services
        ]
        top_agents = (
            TicketLog.objects.filter(assigned_agent__isnull=False)
            .values('assigned_agent__first_name', 'assigned_agent__last_name')
            .annotate(ticket_count=Count('ticket_id', distinct=True))
            .order_by('-ticket_count')[:5]
        )


        top_5_agents = [
            {
                "agent_name": f"{a['assigned_agent__first_name']} {a['assigned_agent__last_name']}",
                "ticket_count": a["ticket_count"],
            }
            for a in top_agents
        ]
        total_open_tickets = TicketLog.objects.filter(ticket_state__state_id__in=[1, 4, 6, 7, 8]).values('ticket_id').distinct().count()
        total_closed_tickets = TicketLog.objects.filter(ticket_state__state_id__in=[2, 3, 5, 9, 10]).values('ticket_id').distinct().count()
        dashboard_data = {
            "total_users": total_users,
            "total_tickets": total_tickets,
            "total_open_tickets": total_open_tickets,
            "total_closed_tickets": total_closed_tickets,
            "tasks_today": tasks_today,
            "top_5_services": top_5_services,
            "top_5_agents": top_5_agents,
        }
        return Response({
            "status": True,
            "status_code": 200,
            "data": dashboard_data,
        })
