from langchain_chroma import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import time

def search_similarity(query, vector_store:Chroma, k:int=3) -> str:
    """Search for similar documents in the vector store."""
    return vector_store.similarity_search(query, k=k)[0].page_content

def get_prompt() -> PromptTemplate:
    """Get the prompt for the chat model."""
    return PromptTemplate(
        template="""
        You are a helpful assistant. Answer the question based on the context provided.
        Job description: {context}
        Self-Instruction: {self_instruction}
        Question: {query}
        Answer the Korean question in Korean.:
        """,
        input_variables=["context", "self_instruction", "query"]
    )

def get_answer(prompt:PromptTemplate, ollama:ChatOllama, context:str, self_instruction:str, query:str) :
    """Get the answer from the chat model."""
    chain = prompt | ollama | StrOutputParser()
    for token in chain.stream({"context": context, "self_instruction": self_instruction, "query": query}):
        yield token
        time.sleep(0.05) 


