from django.contrib import admin

from .models import Agent, Type, Service, TicketPriority, SqlCommand, TicketLog, TicketState


admin.site.register(Agent)
admin.site.register(Type)
admin.site.register(Service)
admin.site.register(TicketPriority)
admin.site.register(SqlCommand) 
admin.site.register(TicketLog) 
admin.site.register(TicketState) 
    