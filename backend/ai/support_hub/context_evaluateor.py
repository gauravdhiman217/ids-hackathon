"""
Relevance evaluation module for assessing retrieved context quality.

This module provides functionality to determine if retrieved context
contains relevant information to answer a given query.
"""

from typing import Optional

from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

from .model_hub import get_model


class Classification(BaseModel):
    """Schema for relevance classification results."""

    is_relevant: bool = Field(
        ..., description="Whether the statement is relevant or not"
    )
    reason: str = Field(
        ..., description="Brief explanation of why the context is or isn't relevant"
    )


class RelevanceEvaluator:
    """Evaluates whether retrieved context is relevant to a query."""

    EVALUATION_TEMPLATE = """You are a relevance evaluator. Your task is to determine if the retrieved context contains information that can help answer the given query.

Query:
```text
{query}
```

Retrieved Context:
```text 
{retrieved_context}
```

Analyze the retrieved context and determine if it contains relevant information to answer the query. Consider:
- Does the context directly address the query topic?
- Does it contain facts, data, or information related to the query?
- Can the context be used to formulate a meaningful answer?

{format_instructions}

Be strict in your evaluation. Only mark as relevant if the context can genuinely help answer the query."""

    def __init__(self, model: Optional[BaseLanguageModel] = None):
        """
        Initialize the relevance evaluator.

        Args:
            model: Language model to use. If None, uses default from model_hub.
        """
        self.model = model or get_model()
        self.parser = PydanticOutputParser(pydantic_object=Classification)
        self.prompt = PromptTemplate(
            template=self.EVALUATION_TEMPLATE,
            input_variables=["query", "retrieved_context"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )
        self.chain = self.prompt | self.model | self.parser

    def evaluate(self, query: str, retrieved_context: str) -> Classification:
        """
        Evaluate relevance of retrieved context for a query.

        Args:
            query: The user's query.
            retrieved_context: The retrieved context to evaluate.

        Returns:
            Classification object with is_relevant flag and reason.
        """
        return self.chain.invoke(
            {"query": query, "retrieved_context": retrieved_context}
        )

    async def aevaluate(self, query: str, retrieved_context: str) -> Classification:
        """
        Asynchronously evaluate relevance of retrieved context.

        Args:
            query: The user's query.
            retrieved_context: The retrieved context to evaluate.

        Returns:
            Classification object with is_relevant flag and reason.
        """
        return await self.chain.ainvoke(
            {"query": query, "retrieved_context": retrieved_context}
        )


# Convenience function for one-off evaluations
async def evaluate_relevance(
    query: str, retrieved_context: str, model: Optional[BaseLanguageModel] = None
) -> Classification:
    """
    Evaluate relevance of retrieved context for a query.

    Args:
        query: The user's query.
        retrieved_context: The retrieved context to evaluate.
        model: Optional language model to use.

    Returns:
        Classification object with is_relevant flag and reason.
    """
    evaluator = RelevanceEvaluator(model=model)
    evaluated_class = await evaluator.aevaluate(query, retrieved_context)
    return evaluated_class.model_dump()
