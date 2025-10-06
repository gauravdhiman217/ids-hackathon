from pydantic import BaseModel, Field
from .categories_probabilities import CategoriesProbabilities
from .priority import Priority


class TicketPrediction(BaseModel):
    categories_probabilities: CategoriesProbabilities = Field(
        ...,
        description="Probability scores for each ticket category."
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
