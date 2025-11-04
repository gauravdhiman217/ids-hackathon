from django.db import models


    
class Type(models.Model):
    type_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    is_valid = models.BooleanField(default=True)


    def __str__(self):
        return self.name
    
class Service(models.Model):
    service_id = models.IntegerField(primary_key=True)
    service_name = models.CharField(max_length=100)
    sla_id = models.IntegerField()
    sla_name = models.CharField(max_length=200)
    first_response_time = models.IntegerField()
    update_time = models.IntegerField()
    solution_time = models.IntegerField()
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.service_name

class Agent(models.Model):
    agent_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"

class TicketPriority(models.Model):
    priority_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    is_valid = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
class SqlCommand(models.Model):
    command_id = models.AutoField(primary_key=True)
    command_text = models.TextField()
    description = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Command {self.command_id}: {self.description or 'No Description'}"
    
    
class TicketState(models.Model):
    state_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}-{self.state_id}"
    

class TicketLog(models.Model):
    EVENT_CHOICES = [
    ('webhook', 'Webhook'),
    ('auto-assign', 'Auto Assign'),
    ('manual-update', 'Manual Update'),
    ('type-update', 'Type Update'),
    ('service-update', 'Service Update'),
    ('priority-update', 'Priority Update'),
    ('owner-update', 'Owner Update'),
    ('state-update', 'State Update'),
    ('closed', 'Ticket Closed'),
]
    ticket_id = models.IntegerField()
    ticket_owner = models.CharField(max_length=250, null=True, blank=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True) 
    priority = models.ForeignKey(TicketPriority, on_delete=models.SET_NULL, null=True)
    assigned_agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    ticket_override = models.BooleanField(default=False)
    entry_type = models.CharField(max_length=50, choices=EVENT_CHOICES, default='auto-assign')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ticket_state = models.ForeignKey(TicketState, on_delete=models.SET_NULL, null=True)
    ticket_hash = models.CharField(max_length=50, null=True, blank=True)


    def __str__(self):
        return f"Ticket {self.ticket_id}: {self.entry_type} - {self.priority} - {self.assigned_agent or 'Unassigned'}"
    

