from pydantic import BaseModel, Field

from .priority import Priority
from .services_probabilities import ServicesProbabilities
from .types_probabilities import TicketTypeProbabilities


class TicketPrediction(BaseModel):
    services_probabilities: ServicesProbabilities = Field(
        ..., description="Probability scores for ticket service."
    )
    type_probabilities: TicketTypeProbabilities = Field(
        ..., description="Probability scores for ticket type."
    )
    priority: Priority = Field(
        ...,
        description=(
            "Priority of the ticket, from 1 to 5:\n"
            "1 = Very High\n"
            "2 = High\n"
            "3 = Normal\n"
            "4 = Low\n"
            "5 = Very Low"
        ),
    )
