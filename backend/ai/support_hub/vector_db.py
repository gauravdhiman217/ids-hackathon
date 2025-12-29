from dotenv import load_dotenv
from pinecone import Pinecone

from .embedding_factory import embeddings

load_dotenv()
pc = Pinecone()
index = pc.Index(name="faqs")

from langchain_pinecone import PineconeVectorStore

vector_store = PineconeVectorStore(index=index, embedding=embeddings)

from langchain.retrievers.multi_query import MultiQueryRetriever

from .model_hub import model

question = "Forget"
retriever_from_llm = MultiQueryRetriever.from_llm(
    retriever=vector_store.as_retriever(
        search_type="mmr", search_kwargs={"k": 4, "lambda_mult": 0.5}
    ),
    llm=model,
)









