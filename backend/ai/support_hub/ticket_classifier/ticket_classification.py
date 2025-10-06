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

    predicted_type = opt.type_probabilities.top_category()
    predicted_type = predicted_type[0].split("_")
    print(predicted_type)
    type_name = " ".join(predicted_type[:-2])

    predicted_service = opt.services_probabilities.top_category()
    service = predicted_service[0].split("_")
    service_name = " ".join(service[:-2])
    return {
        "ticket_class": {
            "service": {"service_name": service_name, "service_id": service[-1]},
            "type": {"type_name": type_name, "type_id": predicted_type[-1]},
        },
        "priority": opt.priority,
    }
