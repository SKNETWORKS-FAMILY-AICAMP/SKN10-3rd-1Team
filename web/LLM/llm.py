from langchain.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import time
from langchain_openai import OpenAIEmbeddings

def load_vector_store() -> FAISS:
    db = FAISS.load_local(
        folder_path="../data/faiss_db",
        index_name="faiss_index",
        embeddings=OpenAIEmbeddings(model="text-embedding-3-small"),
        allow_dangerous_deserialization=True,
    )

    return db

def search_similarity(self_instruction:str, vector_store:FAISS, k:int=3) -> str:
    """Search for similar documents in the vector store."""
    return vector_store.similarity_search(self_instruction, k=k)[0].page_content

def get_prompt_template(tavily=False) -> PromptTemplate:
    """Get the prompt for the chat model."""
    if tavily:
        return PromptTemplate(
            template="""
            You are a helpful assistant. Answer the question based on the context provided.
            Tavily search: {context}
            Question: {query}
            Answer the Korean question in Korean.:
            """,
            input_variables=["context", "query"]
        )
    else:
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

def get_answer(llm, context:str, self_instruction:str, query:str, prompt=get_prompt_template()) :
    """Get the answer from the chat model."""
    chain = prompt | llm | StrOutputParser()
    for token in chain.stream({"context": context, "self_instruction": self_instruction, "query": query}):
        yield token
        time.sleep(0.05) 


