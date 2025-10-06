# serializers.py
from rest_framework import serializers
from .models import Agent, Service, Type, TicketPriority
from django.db.models import Count
from datetime import datetime, timedelta

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'

class AgentSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['role']





class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class TicketPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPriority
        fields = '__all__'



class DashboardSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    total_tickets = serializers.IntegerField()
    tasks_today = serializers.IntegerField()
    top_5_services = serializers.ListField()
    top_5_ticket_owners = serializers.ListField()