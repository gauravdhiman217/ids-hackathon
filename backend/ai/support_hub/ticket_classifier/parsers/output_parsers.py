from langchain.output_parsers import OutputFixingParser
from langchain_core.output_parsers import PydanticOutputParser
from langsmith import traceable

from ..models.role_prediction import Role
from ..models.ticket_prediction import TicketPrediction


@traceable
def get_pydantic_parser():
    return PydanticOutputParser(pydantic_object=TicketPrediction)


@traceable
def get_pydantic_role_parser():
    return PydanticOutputParser(pydantic_object=Role)


@traceable
def get_output_fixing_parser(llm, parser):
    return OutputFixingParser.from_llm(parser=parser, llm=llm)
