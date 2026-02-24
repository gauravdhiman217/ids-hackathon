from langchain_core.prompts import PromptTemplate
from langsmith import traceable
from langfuse import observe

@traceable
@observe
def get_ticket_classification_prompt(format_instructions: str) -> PromptTemplate:
    template = """
You are an IT support ticket classifier.

Given the ticket, provide the following:

1. service_probabilities: a probability score (in percentage) for each ticket service that represents how likely the ticket belongs to that service.
   - All service probabilities must sum up to 100%.
   - No two services should have the same probability score.

2. priority: one of the following Enum values (VeryHigh = 1, High = 2, Normal = 3, Low = 4, VeryLow = 5), representing how important it is to resolve the issue quickly so that there are no work blockers or wasted time.

3. type_probabilities: a probability score (in percentage) for each ticket type that represents how likely the ticket belongs to that type.
   - All type probabilities must sum up to 100%.
   - No two types should have the same probability score.

{format_instructions}

Ticket:
```
{ticket}
```
"""

    return PromptTemplate(
        template=template,
        input_variables=["ticket"],
        partial_variables={"format_instructions": format_instructions},
    )


@traceable
@observe
def get_ticket_classification_prompt_roles(format_instructions: str) -> PromptTemplate:
    template = """
You are an IT support ticket classifier.

Given the ticket, provide the following:

role: a single resolver role to assign this ticket to.
   - Return exactly one string that matches character-for-character one of the provided roles.
   - Do not invent or modify role names.
   - If multiple roles could apply, choose the most specialized technical role aligned with the primary action implied by the ticket.
   - If unable to confidently select an exact match from the provided roles, return "Manager" by default.

{format_instructions}

Ticket:
```
{ticket}
```
"""

    return PromptTemplate(
        template=template,
        input_variables=["ticket"],
        partial_variables={"format_instructions": format_instructions},
    )
