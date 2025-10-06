from langsmith import traceable

from ..model_hub import get_model
from .parsers.output_parsers import (get_output_fixing_parser,
                                     get_pydantic_parser)
from .prompts.ticket_prompt import get_ticket_classification_prompt


@traceable
def run_ticket_classification(ticket: str):
    model = get_model()
    base_parser = get_pydantic_parser()
    fixing_parser = get_output_fixing_parser(llm=model, parser=base_parser)

    prompt = get_ticket_classification_prompt(fixing_parser.get_format_instructions())

    # Compose prompt + model callable
    prompt_and_model = prompt | model
    output = prompt_and_model.invoke({"ticket": ticket})

    # Parse output into Pydantic model
    opt = base_parser.invoke(input=output)

    # Print top category and priority
    # print("Top Category:", opt.categories_probabilities.top_category())
    # print("Priority:", opt.priority)
    top_category = opt.categories_probabilities.top_category()
    service = top_category[0].split("_")
    service_name = " ".join(service[:-2])
    return {
        "ticket_class": {"service_name": service_name, "service_id": service[-1]},
        "priority": opt.priority,
    }
