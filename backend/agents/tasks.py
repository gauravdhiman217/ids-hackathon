from core.base import EmailSender
from celery import shared_task
from .utils import DatabaseSync, ProcessTicket
from .models import Agent, Type, Service, TicketPriority, SqlCommand, TicketLog, TicketState, Location, Roster
from .serializers import AgentSerializer, TypeSerializer, ServiceSerializer, TicketPrioritySerializer
from markdown import markdown

from celery import group
from datetime import datetime, date, time


BODY = """
    Dear {0},

    Reply for your Ticket Number {1}
    
    {2}


    AI Support System
    IDS Infotech Ltd.
    website: https://www.idsil.com

    We cannot promise that we will always be perfect. What we can promise is that if something goes wrong we will rise to the occasion, 
    take action, resolve the issue and accept responsibility.

"""


@shared_task
def process_ticket_data(ticket_id):
        print(f"Processing ticket data for ticket ID: {ticket_id}")
        ticket_processor = ProcessTicket()
        ticket = ticket_processor.fetch_ticket(ticket_id)
        if ticket:
            ticket_obj = TicketLog.objects.filter(ticket_id=ticket_id).order_by('-created_at').first()
            # if ticket_obj:
            #     print(f"Ticket with ID {ticket_id} already exists. Skipping creation.")
            #     ticket_processor.update_ticket_log(ticket_obj.id, ticket)
            #     return {"ticket_id": ticket_id, "status": "updating existing ticket"}
            ticket_processor.store_ticket_log(ticket_id, ticket, entry_type="webhook")
            

            process_ticket_embedding.delay(ticket_id)
            
            # job = group(process_ticket_embedding.s(ticket_id), process_ticket_ai.s(ticket_id))
            # job.apply_async()
        return {"ticket_id": ticket_id, "status": "processed"}

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def process_ticket_embedding(self, ticket_id):
    try:
        from ai.support_hub.rag_pipeline import create_rag_pipeline
        print(f"Processing ticket embedding for ticket ID: {ticket_id}")
        ticket = TicketLog.objects.filter(ticket_id=ticket_id).order_by('-created_at').first()
        if ticket:
            answer = create_rag_pipeline(f"{ticket.title} \n\n {ticket.body}")
            # answer = {"answer_found": True, "answer": "This is a placeholder answer from RAG pipeline."}
            print(f"Ticket answer Result: {answer}")
            _email_send_ai(ticket, answer)
            return answer
    except Exception as e:
        print(f"Error processing ticket ID {ticket_id}: {e}")
        # TicketLog.objects.filter(ticket_id=ticket_id).delete()
        self.retry(exc=e, countdown=2 ** self.request.retries)

def _email_send_ai(ticket, answer):
    subject = f"RE: [Ticket#{ticket.ticket_hash}] {ticket.title}"
    reply = "Your e-mail will be answered in short while. Please wait for a little while. We will get back to you as soon as possible."
    if answer.get("answer_found", False):
        html = markdown(answer.get("answer", ""))
        reply = html
    body = BODY.format(ticket.ticket_owner.split("@")[0], ticket.ticket_hash , reply)
    data = fetch_email_mime(ticket)
    emailSender = EmailSender()
    emailSender.send_ai_email(subject, body, ticket.ticket_owner, mime_data=data)

def fetch_email_mime(ticket):
    SQL = f"""
        SELECT  m.* FROM article a join article_data_mime m on a.id = m.article_id WHERE a.ticket_id = {ticket.ticket_id} ORDER BY m.create_time LIMIT 1;
    """
    db_sync = DatabaseSync()
    data = db_sync.fetch_one(SQL)
    if data:
        print("Email MIME data found.", data)
    return data

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def process_ticket_ai(self, ticket_id):
    # return "Skipping now"
    try:
        from ai.support_hub.ticket_classifier.ticket_classification import run_ticket_classification
        print(f"Processing ticket data with AI for ticket ID: {ticket_id}")
        ticket = TicketLog.objects.filter(ticket_id=ticket_id).order_by('-created_at').first()
        if ticket:
            classification = run_ticket_classification(f"{ticket.title} \n\n {ticket.body}")
            print(f"AI Classification Result: {classification}")
            priority = classification.get('priority', None)
            role = classification.get('ticket_class', {}).get("role", None)
            
            # Allocate agent based on queue and role
            agent = _get_agent_by_queue_and_role(ticket.ticket_queue, role)
            
            print(f"Assigned Agent ID: '{agent}' Priority: {priority}")
            if classification:
                new_ticket = TicketLog.objects.create(
                    ticket_id=ticket.ticket_id,
                    title=ticket.title,
                    body=ticket.body,
                    ticket_owner = ticket.ticket_owner,
                    ticket_hash = ticket.ticket_hash,
                    type=Type.objects.filter(type_id=classification.get('ticket_class', {}).get("type", {}).get("type_id", 0)).first(),
                    service=Service.objects.filter(service_id=classification.get('ticket_class', {}).get("service", {}).get("service_id", 0)).first(),
                    priority=TicketPriority.objects.filter(priority_id=priority).first() if priority else None,
                    entry_type="auto-assign",
                    ticket_state=TicketState.objects.filter(state_id=1).first(),  # Assuming 1 is the ID for 'New' state
                    assigned_agent=Agent.objects.filter(agent_id=agent).first() if agent else None,
                    ticket_queue=ticket.ticket_queue,
                )
                process_ticket = ProcessTicket()
                process_ticket.update_ticket(
                    ticket_id,
                    TypeID= new_ticket.type.type_id ,
                    ServiceID= new_ticket.service.service_id ,
                    PriorityID= classification.get('priority', 3),
                    OwnerID = agent if agent else None,
                    SLAID = new_ticket.service.sla_id if new_ticket.service else None,
                    )
    except Exception as e:
        print(f"Error processing ticket ID {ticket_id}: {e}")
        TicketLog.objects.filter(ticket_id=ticket_id).delete()
        self.retry(exc=e, countdown=2 ** self.request.retries)


def _get_agent_by_queue_and_role(queue_id, role):
    """
    Fetch an agent based on queue, role, and today's roster shift timing.
    
    Logic:
    1. Find the location linked to the given queue_id
    2. Filter agents deployed on that location with matching role
    3. Check their roster for TODAY (current week) and today's day status
    4. Prefer agents currently on-shift (status='ON' and within start/end times)
    5. Fallback to any matching agent if none are on-shift
    6. Default to agent_id=1 if no agents found
    
    Args:
        queue_id (int or str): The queue ID to search for
        role (str): The role to match (case-insensitive)
    
    Returns:
        int: agent_id if found, otherwise default agent id=1
    """
    if not role:
        role = "Admin Otrs"
    
    role = role.strip()
    
    # Step 1: Find location(s) linked to this queue
    locations = Location.objects.filter(queue=str(queue_id))
    
    if not locations.exists():
        print(f"No location found for queue {queue_id}. Defaulting to agent_id=1.")
        return 1
    
    # Step 2: Get agents deployed on those locations with matching role
    agents = Agent.objects.filter(
        location__in=locations,
        role__icontains=role,
        is_valid=True
    )

    if agents.count() < 1:
        print(f"No agent found for queue {queue_id} with role '{role}'. Defaulting to agent_id=1.")
        return 1
    available_agent_ids = set()
    today = datetime.now().strftime("%a").lower()
    available_agents = Agent.objects.raw(f""" SELECT aa.agent_id FROM agents_agent aa 
                               join agents_roster ar on ar.agent_id = aa.agent_id 
                               WHERE {today}_status = 'ON' and {today}_end > ((now() AT TIME ZONE 'Asia/Kolkata')::time) 
                               and {today}_start < (now() AT TIME ZONE 'Asia/Kolkata')::time;""")
    for agent in available_agents:
        available_agent_ids.add(agent.agent_id)

    print(f"Available agents on shift today for role '{role}': {available_agent_ids}")
    if available_agent_ids:
        avail_qs = agents.filter(agent_id__in=available_agent_ids)
        if avail_qs.count() == 0:
            print(f"No agents on shift today for role '{role}'. Falling back to any matching agent.")
            return 1
        elif avail_qs.count() == 1:
            return avail_qs.first().agent_id
        return avail_qs.order_by('?').first().agent_id

    # No agents available today per roster -> fallback to any matching agent
    if agents.count() == 1:
        return agents.first().agent_id
    return agents.order_by('?').first().agent_id


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