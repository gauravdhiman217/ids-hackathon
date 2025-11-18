import os
from pyotrs import Client
import mysql.connector
from .models import TicketLog, Agent, Type, Service, TicketPriority, TicketState
from datetime import datetime

class DatabaseSync:
    def __init__(self):
        self.host = os.getenv("OTRS_DB_HOST", "192.168.10.97")
        self.user = os.getenv("OTRS_DB_USER", "django")
        self.password = os.getenv("OTRS_DB_PASSWORD", "DevSsb")
        self.database = os.getenv("OTRS_DB_NAME", "otrs")
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Database connection established.")
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")

    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")

    def execute_query(self, query, params=None):
        try:
            self.connect()
            self.cursor.execute(query, params)
            self.connection.commit()
            print("Query executed successfully.")
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            self.connection.rollback()
            return None
        finally:
            self.disconnect()

    def fetch_one(self, query, params=None):
        try:
            self.connect()
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()
            return result
        except mysql.connector.Error as err:
            print(f"Error fetching one: {err}")
            return None
        finally:
            self.disconnect()

    def fetch_all(self, query, params=None):
        try:
            self.connect()
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error fetching all: {err}")


class ProcessTicket:
    def __init__(self):
        self.userName = os.getenv("OTRS_USER", "root@localhost")
        self.password = os.getenv("OTRS_PASSWORD", "DemoDemo11")
        self.url = os.getenv("OTRS_URL", "http://192.168.10.97")
        self.client = Client(
            self.url,
            self.userName,
            self.password,
        )
        self.client.session_restore_or_create()

    def fetch_ticket(self, ticket_id):
        """Fetch ticket data from the ticketing system."""
        ticket = self.client.ticket_get_by_id(ticket_id, articles=True)
        return ticket

    def update_ticket(self, ticket_id, **kwargs):
        """
        Update ticket data in the ticketing system.
        
        kwargs can include fields like Title, QueueID, StateID, PriorityID, OwnerID, TypeID, ServiceID
        
        """
        self.client.session_restore_or_create()
        update_data = {}
        for key, val in kwargs.items():
            update_data[key] = val
        if update_data:
            self.client.ticket_update(ticket_id, **update_data)
            return True
        return False
    
    def store_ticket_log(self, ticket_id, ticket_object, entry_type="auto-assign"):
        """
        Store a log entry for a ticket.
        
        log_entry should be a dictionary with keys like Title, Body, TypeID, etc.
        """
        ticket = TicketLog.objects.filter(ticket_id=ticket_object.field_get("TicketID")).order_by('-created_at').first()
        print(f"Ticket Owner {ticket_object.field_get("CustomerUserID")} || {ticket_object.field_get("TicketNumber")}")
        if not ticket:
            TicketLog.objects.create(
                ticket_id=ticket_id,
                title=ticket_object.field_get('Title'),
                body= ticket_object.articles[0].field_get('Body') if ticket_object.articles else '',
                type = Type.objects.filter(type_id=ticket_object.field_get('TypeID')).first(),
                service = Service.objects.filter(service_id=ticket_object.field_get('ServiceID')).first() if ticket_object.field_get('ServiceID') else None,
                priority = TicketPriority.objects.filter(priority_id=ticket_object.field_get('PriorityID')).first() if ticket_object.field_get('PriorityID') else None,
                assigned_agent = Agent.objects.filter(agent_id=ticket_object.field_get('OwnerID')).first() if ticket_object.field_get('OwnerID') else None,
                entry_type = entry_type,
                ticket_hash = ticket_object.field_get('TicketNumber'),
                ticket_owner = ticket_object.field_get("CustomerUserID"),
                ticket_queue = ticket_object.field_get('QueueID'),
                ticket_state = TicketState.objects.filter(state_id=ticket_object.field_get('StateID')).first() if ticket_object.field_get('StateID') else None,
            )
            return True
        return False
    
    def update_ticket_log(self, log_id, ticket_object):
        """
        Update a log entry for a ticket.
        
        log_entry should be a dictionary with keys like Title, Body, TypeID, etc.
        """
        try:
            log_entry = TicketLog.objects.get(id=log_id)
            log_entry.title = ticket_object.field_get('Title')
            log_entry.body = ticket_object.articles[0].field_get('Body') if ticket_object.articles else ''
            ticket_type = Type.objects.filter(type_id=ticket_object.field_get('TypeID')).first()
            if log_entry.type != ticket_type:
                self._create_ticket(
                    log_entry, 
                    entry_type="type-update", 
                    type=ticket_type, 
                    service=log_entry.service, 
                    priority=log_entry.priority, 
                    assigned_agent=log_entry.assigned_agent, 
                    ticket_state=log_entry.ticket_state
                )
            ticket_service = Service.objects.filter(service_id=ticket_object.field_get('ServiceID')).first() if ticket_object.field_get('ServiceID') else None
            if log_entry.service != ticket_service:
                self._create_ticket(
                    log_entry, 
                    entry_type="service-update", 
                    type=log_entry.type, 
                    service=ticket_service, 
                    priority=log_entry.priority, 
                    assigned_agent=log_entry.assigned_agent, 
                    ticket_state=log_entry.ticket_state
                )
            ticket_priority = TicketPriority.objects.filter(priority_id=ticket_object.field_get('PriorityID')).first() if ticket_object.field_get('PriorityID') else None
            if log_entry.priority != ticket_priority:
                self._create_ticket(
                    log_entry, 
                    entry_type="priority-update", 
                    type=log_entry.type, 
                    service=log_entry.service, 
                    priority=ticket_priority, 
                    assigned_agent=log_entry.assigned_agent, 
                    ticket_state=log_entry.ticket_state
                )
            ticket_assigned_agent = Agent.objects.filter(agent_id=ticket_object.field_get('OwnerID')).first() if ticket_object.field_get('OwnerID') else None
            if log_entry.assigned_agent != ticket_assigned_agent:
                self._create_ticket(
                    log_entry, 
                    entry_type="owner-update", 
                    type=log_entry.type, 
                    service=log_entry.service, 
                    priority=log_entry.priority, 
                    assigned_agent=ticket_assigned_agent, 
                    ticket_state=log_entry.ticket_state
                )
            ticket_state = TicketState.objects.filter(state_id=ticket_object.field_get('StateID')).first() if ticket_object.field_get('StateID') else None
            if log_entry.ticket_state != ticket_state:
                self._create_ticket(
                    log_entry, 
                    entry_type="state-update", 
                    type=log_entry.type, 
                    service=log_entry.service, 
                    priority=log_entry.priority, 
                    assigned_agent=log_entry.assigned_agent, 
                    ticket_state=ticket_state
                )
            log_entry.save()
            return True
        except TicketLog.DoesNotExist:
            print(f"Log entry with ID {log_id} does not exist.")
            return False

    def _create_ticket(self, log_entry, entry_type, type, service, priority, assigned_agent, ticket_state):
        """
        Internal method to create a ticket in the ticketing system.
        
        ticket_data should be a dictionary with keys like Title, QueueID, StateID, PriorityID, OwnerID, TypeID, ServiceID
        
        """
        TicketLog.objects.create(
            ticket_id=log_entry.ticket_id,
            title=log_entry.title,
            body=log_entry.body,
            type=type,
            service=service,
            priority=priority,
            assigned_agent=assigned_agent,
            entry_type=entry_type,
            ticket_state=ticket_state,
            updated_at=datetime.now()
        )