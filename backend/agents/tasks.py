from celery import shared_task


@shared_task
def process_ticket_data(ticket_id):
    print(f"Processing ticket data for ticket ID: {ticket_id}")
    return {"ticket_id": ticket_id, "status": "processed"}