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
    
    