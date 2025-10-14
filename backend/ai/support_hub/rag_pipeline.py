from typing import List, Optional

import GPUtil
# import torch
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import VectorStore
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langgraph.graph import START, StateGraph
from pinecone import Pinecone
from typing_extensions import TypedDict

from .context_evaluateor import evaluate_relevance
from .model_hub import get_model
from .retriever_factory import create_multi_query_retriever

EMBEDDING_MODEL_NAME = "BAAI/bge-large-en-v1.5"
# Set device for embeddings
# device = "cuda" if torch.cuda.is_available() else "cpu"
# Get a list of all GPUs

device = "cuda" if GPUtil.getGPUs() else "cpu"

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL_NAME, model_kwargs={"device": device}
)


# State definition
class RAGState(TypedDict):
    """State schema for RAG pipeline."""

    question: str
    context: List[Document]
    answer: str
    answer_found: bool


class RAGConfig:
    """Configuration for RAG pipeline components."""

    # Prompt template
    ANSWER_TEMPLATE = """You are an IT support assistant. Use the provided knowledge base context to answer the support query.

Knowledge Base Context:
{context}

User Query: {question}

Instructions:
- Provide a clear, actionable answer based on the context
- If troubleshooting steps are mentioned, list them in order
- Keep technical language appropriate for the user's level
- Be helpful and professional"""

    # Embedding model configuration
    # EMBEDDING_MODEL_NAME = "BAAI/bge-large-en-v1.5"

    # Pinecone configuration
    PINECONE_INDEX_NAME = "faqs"

    def __init__(
        self,
        embedding_model_name: Optional[str] = None,
        pinecone_index_name: Optional[str] = None,
        answer_template: Optional[str] = None,
    ):
        """
        Initialize RAG configuration.

        Args:
            embedding_model_name: Name of HuggingFace embedding model.
            pinecone_index_name: Name of Pinecone index.
            answer_template: Custom prompt template for answer generation.
        """
        # self.embedding_model_name = embedding_model_name or self.EMBEDDING_MODEL_NAME
        self.pinecone_index_name = pinecone_index_name or self.PINECONE_INDEX_NAME
        self.answer_template = answer_template or self.ANSWER_TEMPLATE


class RAGPipeline:
    """End-to-end RAG pipeline using LangGraph."""

    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        llm: Optional[BaseLanguageModel] = None,
        config: Optional[RAGConfig] = None,
    ):
        """
        Initialize RAG pipeline.

        Args:
            vector_store: Vector store for document retrieval. If None, creates Pinecone store.
            llm: Language model for generation. If None, uses default from model_hub.
            config: RAG configuration. If None, uses default configuration.
        """
        self.config = config or RAGConfig()
        self.llm = llm or get_model()
        self.vector_store = vector_store or self._create_default_vector_store()
        self.prompt = PromptTemplate.from_template(self.config.answer_template)
        self.graph = self._build_graph()

    def _create_default_vector_store(self) -> VectorStore:
        """Create default Pinecone vector store with HuggingFace embeddings."""
        load_dotenv()

        # # Set device for embeddings
        # device = "cuda" if torch.cuda.is_available() else "cpu"

        # # Initialize embeddings
        # embeddings = HuggingFaceEmbeddings(
        #     model_name=self.config.embedding_model_name, model_kwargs={"device": device}
        # )

        # Initialize Pinecone
        pc = Pinecone()
        index = pc.Index(self.config.pinecone_index_name)

        return PineconeVectorStore(index=index, embedding=embeddings)

    def _retrieve(self, state: RAGState) -> dict:
        """
        Retrieve relevant documents for the question.

        Args:
            state: Current RAG state.

        Returns:
            Dictionary with retrieved context documents.
        """
        retriever = create_multi_query_retriever(vector_store=self.vector_store)
        retrieved_docs = retriever.invoke(state["question"])
        return {"context": retrieved_docs}

    async def _generate(self, state: RAGState) -> dict:
        """
        Generate answer from retrieved context.

        Args:
            state: Current RAG state with retrieved context.

        Returns:
            Dictionary with answer_found flag and answer content.
        """
        # Format context documents
        docs_content = (
            "\n```"
            + "\n\n".join(doc.page_content for doc in state["context"])
            + "\n```"
        )

        # Evaluate context relevance
        evaluated_class = await evaluate_relevance(
            query=state["question"], retrieved_context=docs_content
        )

        # Return early if context is not relevant
        if not evaluated_class.get("is_relevant"):
            return {"answer_found": False}

        # Generate answer
        messages = self.prompt.invoke(
            {"question": state["question"], "context": docs_content}
        )
        response = self.llm.invoke(messages)

        return {"answer_found": True, "answer": response.content}

    def _build_graph(self) -> StateGraph:
        """
        Build LangGraph pipeline.

        Returns:
            Compiled StateGraph for RAG pipeline.
        """
        graph_builder = StateGraph(RAGState).add_sequence(
            [self._retrieve, self._generate]
        )
        graph_builder.add_edge(START, "_retrieve")
        return graph_builder.compile()

    async def ainvoke(self, question: str) -> dict:
        """
        Asynchronously invoke RAG pipeline.

        Args:
            question: User question to answer.

        Returns:
            Dictionary containing answer_found flag and answer content.
        """
        result = await self.graph.ainvoke({"question": question})
        return {
            "answer_found": result.get("answer_found", False),
            "answer": result.get("answer"),
        }

    def invoke(self, question: str) -> dict:
        """
        Synchronously invoke RAG pipeline.

        Args:
            question: User question to answer.

        Returns:
            Dictionary containing answer_found flag and answer content.
        """
        result = self.graph.invoke({"question": question})
        return {
            "answer_found": result.get("answer_found", False),
            "answer": result.get("answer"),
        }

    async def stream(self, question: str):
        """
        Stream RAG pipeline execution with intermediate states.

        Args:
            question: User question to answer.

        Yields:
            Intermediate states during pipeline execution.
        """
        async for state in self.graph.astream({"question": question}):
            yield state


# Factory function for easy instantiation
async def create_rag_pipeline(
    ticket: str,
    vector_store: Optional[VectorStore] = None,
    llm: Optional[BaseLanguageModel] = None,
    config: Optional[RAGConfig] = None,
) -> RAGPipeline:
    """
    Create a RAG pipeline instance.

    Args:
        vector_store: Custom vector store. If None, uses default Pinecone.
        llm: Custom language model. If None, uses default from model_hub.
        config: Custom RAG configuration. If None, uses defaults.

    Returns:
        Configured RAGPipeline instance.
    """
    pipeline = RAGPipeline(vector_store=vector_store, llm=llm, config=config)
    result = await pipeline.ainvoke(ticket)
    return {"answer_found": result.get("answer_found"), "answer": result.get("answer")}
