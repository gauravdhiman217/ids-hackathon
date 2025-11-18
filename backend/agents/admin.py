from django.contrib import admin

from .models import (Agent, Roster, Type, Service, TicketPriority, SqlCommand, TicketLog, TicketState, Location)
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import path
from datetime import date, timedelta
from .models import Agent, Roster
from .forms import RosterForm
# admin.site.register(Agent)
admin.site.register(Type)
admin.site.register(Service)
admin.site.register(TicketPriority)
admin.site.register(SqlCommand) 
admin.site.register(TicketLog) 
admin.site.register(TicketState) 
admin.site.register(Location)
    


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('location__name',)

@admin.register(Roster)
class RosterAdmin(admin.ModelAdmin):
    form = RosterForm
    change_form_template = "admin/roster_change_form.html"
    list_display = ('agent', 'week_start')
    search_fields = ('agent__name',)
    list_filter = ('week_start', 'agent')

    def get_week_dates_for(self, week_start):
        """Return list of date objects for Mon..Sun given a week_start (date)."""
        if not week_start:
            return []
        return [week_start + timedelta(days=i) for i in range(7)]

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        # Prefer posted week_start (if present) so the header updates on validation errors
        posted_week = None
        if request.method == 'POST':
            posted_week = request.POST.get('week_start')
            # attempt to parse 'YYYY-W##' to date
            if posted_week and '-W' in posted_week:
                try:
                    year, w = posted_week.split('-W')
                    posted_week = date.fromisocalendar(int(year), int(w), 1)
                except Exception:
                    posted_week = None
            else:
                try:
                    # may be ISO date like 2025-02-10
                    posted_week = date.fromisoformat(posted_week)
                except Exception:
                    posted_week = None

        # if editing existing object, get its week_start
        obj_week = None
        if object_id:
            try:
                obj = Roster.objects.get(pk=object_id)
                obj_week = obj.week_start
            except Roster.DoesNotExist:
                obj_week = None

        week_start = posted_week or obj_week
        extra_context['week_dates'] = self.get_week_dates_for(week_start)
        return super().changeform_view(request, object_id, form_url, extra_context=extra_context)
