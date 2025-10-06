from django.contrib import admin

from .models import Agent, Type, Service, TicketPriority, SqlCommand

admin.site.register(Agent)
admin.site.register(Type)
admin.site.register(Service)
admin.site.register(TicketPriority)
admin.site.register(SqlCommand) 
