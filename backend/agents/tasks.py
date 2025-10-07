from celery import shared_task
from .utils import DatabaseSync, ProcessTicket
from .models import Agent, Type, Service, TicketPriority, SqlCommand, TicketLog, TicketState
from .serializers import AgentSerializer, TypeSerializer, ServiceSerializer, TicketPrioritySerializer
from ai.support_hub.ticket_classifier.ticket_classification import run_ticket_classification




@shared_task
def process_ticket_data(ticket_id):
    print(f"Processing ticket data for ticket ID: {ticket_id}")
    ticket_processor = ProcessTicket()
    ticket = ticket_processor.fetch_ticket(ticket_id)
    if ticket:
        ticket_obj = TicketLog.objects.filter(ticket_id=ticket_id).order_by('-created_at').first()
        if ticket_obj:
            print(f"Ticket with ID {ticket_id} already exists. Skipping creation.")
            ticket_processor.update_ticket_log(ticket_obj.id, ticket)
            return {"ticket_id": ticket_id, "status": "updating existing ticket"}
        ticket_processor.store_ticket_log(ticket_id, ticket, entry_type="webhook")
        process_ticket_ai(ticket_id)
    return {"ticket_id": ticket_id, "status": "processed"}

def process_ticket_ai(ticket_id):
    print(f"Processing ticket data with AI for ticket ID: {ticket_id}")
    ticket = TicketLog.objects.filter(ticket_id=ticket_id).order_by('-created_at').first()
    if ticket:
        classification = run_ticket_classification(f"{ticket.title} \n\n {ticket.body}")
        print(f"AI Classification Result: {classification}")
        priority = classification.get('priority', None)
        if classification:
            new_ticket = TicketLog.objects.create(
                ticket_id=ticket.ticket_id,
                title=ticket.title,
                body=ticket.body,
                type=Type.objects.filter(type_id=classification.get('ticket_class', {}).get("type", {}).get("type_id", 0)).first(),
                service=Service.objects.filter(service_id=classification.get('ticket_class', {}).get("service", {}).get("service_id", 0)).first(),
                priority=TicketPriority.objects.filter(priority_id=priority).first() if priority else None,
                entry_type="auto-assign",
                ticket_state=TicketState.objects.filter(state_id=1).first(),  # Assuming 1 is the ID for 'New' state
            )
            process_ticket = ProcessTicket()
            process_ticket.update_ticket(
                ticket_id,
                TypeID= new_ticket.type.type_id ,
                ServiceID= new_ticket.service.service_id ,
                PriorityID= classification.get('priority', 3),
                # StateID= new_ticket.ticket_state.state_id ,
                SLAID = new_ticket.service.sla_id if new_ticket.service else None,
                )

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
        elif command.description == "get_state":
            for state in data:
                state, _ = TicketState.objects.update_or_create(
                    state_id = state[0],
                    name = state[1],
                    defaults={
                        "is_valid": True if state[2] == 1 else False,
                    }
                )

    print("Database synchronization task completed.")
    return {"status": "completed"}