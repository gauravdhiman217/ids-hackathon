from langchain_core.prompts import PromptTemplate
from langsmith import traceable


@traceable
def get_ticket_classification_prompt(format_instructions: str) -> PromptTemplate:
    template = """
You are an IT support ticket classifier.

Given the ticket description, provide the following:

1. **categories_probabilities**: a probability score (in percentage) for each ticket category that represents how likely the ticket belongs to that category.
   - All probabilities must sum up to 100%.
   - No two categories should have the same probability score.

2. **priority**: one of the following Enum values (VeryHigh = 1, High = 2, Normal = 3, Low = 4, VeryLow = 5), representing how important it is to resolve the issue quickly so that there are no work blockers or wasted time.

{format_instructions}

Ticket Description:
```
{ticket}
```
"""

    return PromptTemplate(
        template=template,
        input_variables=["ticket"],
        partial_variables={"format_instructions": format_instructions},
    )
