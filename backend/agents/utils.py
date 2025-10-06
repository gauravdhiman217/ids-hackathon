import os
from pyotrs import Client
import mysql.connector

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
            session_lifetime=600,
            verify_ssl=False,
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
