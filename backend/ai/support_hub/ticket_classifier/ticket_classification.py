from langchain_core.runnables import RunnableParallel
from langsmith import traceable

from ..model_hub import get_model
from .parsers.output_parsers import (get_output_fixing_parser,
                                     get_pydantic_parser,
                                     get_pydantic_role_parser)
from .prompts.ticket_prompt import (get_ticket_classification_prompt,
                                    get_ticket_classification_prompt_roles)


@traceable
def run_ticket_classification(ticket: str):
    model = get_model()

    # for initial 3 classification tasks
    base_parser = get_pydantic_parser()
    fixing_parser = get_output_fixing_parser(llm=model, parser=base_parser)

    # for role classification task
    base_role_parser = get_pydantic_role_parser()
    fixing_role_parser = get_output_fixing_parser(llm=model, parser=base_role_parser)

    prompt = get_ticket_classification_prompt(fixing_parser.get_format_instructions())
    prompt_role = get_ticket_classification_prompt_roles(
        format_instructions=fixing_role_parser.get_format_instructions()
    )

    # Compose prompt + model callable
    prompt_and_model = prompt | model | base_parser
    # output = prompt_and_model.invoke({"ticket": ticket})

    # for role classification task
    prompt_and_model_role = prompt_role | model | base_role_parser
    # output_role = prompt_and_model_role.invoke({"ticket": ticket})

    classifications = RunnableParallel(
        classificationi3=prompt_and_model, classification_role=prompt_and_model_role
    )
    opt = classifications.invoke({"ticket": ticket})
    predicted_service = opt.get(
        "classificationi3"
    ).services_probabilities.top_category()
    service = predicted_service[0].split("_")
    service_name = " ".join(service[:-2])
    # print(service_name,"uuu", service[-1])

    predicted_type = opt.get("classificationi3").type_probabilities.top_category()
    predicted_type = predicted_type[0].split("_")
    # print(predicted_type)
    type_name = " ".join(predicted_type[:-2])
    # print(type_name,"ppp", predicted_type[-1])

    role_opt = opt.get("classification_role")

    return {
        "ticket_class": {
            "service": {"service_name": service_name, "service_id": service[-1]},
            "role": role_opt.role_name.value,
            "type": {"type_name": type_name, "type_id": predicted_type[-1]},
        },
        "priority": opt.get("classificationi3").priority.value,
    }
