import os
from pyotrs import Client
import mysql.connector
from .models import TicketLog, Agent, Type, Service, TicketPriority, TicketState

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
                ticket_state = TicketState.objects.filter(state_id=ticket_object.field_get('StateID')).first() if ticket_object.field_get('StateID') else None,
            )
            return True
        return False