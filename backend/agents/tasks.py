from celery import shared_task
from .utils import DatabaseSync, ProcessTicket
from .models import Agent, Type, Service, TicketPriority, SqlCommand
from .serializers import AgentSerializer, TypeSerializer, ServiceSerializer, TicketPrioritySerializer




@shared_task
def process_ticket_data(ticket_id):
    print(f"Processing ticket data for ticket ID: {ticket_id}")
    ticket_processor = ProcessTicket()
    ticket = ticket_processor.fetch_ticket(ticket_id)
    
    return {"ticket_id": ticket_id, "status": "processed"}


@shared_task
def sync_database():
    print("Starting database synchronization task.")
    db_sync = DatabaseSync()
    cmd = SqlCommand.objects.filter(is_active=True)
    for command in cmd:
        print(f"Executing command: {command.description}")
        data = db_sync.fetch_all(command.command_text)
        if not data:
            print(f"No data found for command: {command.description}")
            continue
        if command.description == "get_users":
            for user in data:
                obj, _ = Agent.objects.update_or_create(
                    agent_id=user[0],
                    user_name=user[1],
                    defaults={
                        "first_name": user[2],
                        "last_name": user[3],
                        "is_valid": True if user[4] == 1 else False,
                    },
                )
        elif command.description == "get_type":
            for type in data:
                type , _ = Type.objects.update_or_create(
                    type_id = type[0],
                    name = type[1],
                    defaults={
                        "is_valid": True if type[2] == 1 else False,
                    }
                )
        elif command.description == "get_priority":
            
            for priority in data:
                priority, _ = TicketPriority.objects.update_or_create(
                    priority_id = priority[0],
                    name = priority[1],
                    defaults={
                        "is_valid": True if priority[2] == 1 else False,
                    }
                )
        elif command.description == "get_services":
            for service in data:
                service, _ = Service.objects.update_or_create(
                    service_id = service[0],
                    service_name = service[1],
                    defaults={
                        "sla_id": service[2],
                        "sla_name": service[3],
                        "first_response_time": service[4],
                        "update_time": service[5],
                        "solution_time": service[6],
                        "is_valid": True if service[7] == 1 else False,
                    }
                )

    print("Database synchronization task completed.")
    return {"status": "completed"}