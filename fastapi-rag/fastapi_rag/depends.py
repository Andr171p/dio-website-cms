from typing import Final

from langchain_core.language_models import BaseChatModel
from langchain_core.retrievers import BaseRetriever
from langchain_gigachat import GigaChat
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
    TextSplitter,
)
from redis.asyncio import Redis

from .settings import settings

TIMEOUT = 120

redis: Final[Redis] = Redis.from_url(settings.redis.url)

md_splitter: Final[MarkdownHeaderTextSplitter] = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("#", "h1")]
)

text_splitter: Final[TextSplitter] = RecursiveCharacterTextSplitter(
    chunk_size=settings.rag.chunk_size,
    chunk_overlap=settings.rag.chunk_overlap,
    length_function=len,
    separators=["\n#"],
)

embeddings = HuggingFaceEmbeddings(
    model_name="deepvk/USER-bge-m3",
)

vectorstore: Final[PineconeVectorStore] = PineconeVectorStore(
    pinecone_api_key=settings.pinecon.api_key_my,
    index_name="rag-index",
    embedding=embeddings,
)

retriever: Final[BaseRetriever] = vectorstore.as_retriever()


llm: Final[BaseChatModel] = GigaChat(
    credentials=settings.gigachat.apikey,
    scope=settings.gigachat.scope,
    model=settings.gigachat.model_name,
    profanity_check=False,
    verify_ssl_certs=False,
    timeout=TIMEOUT,
)
