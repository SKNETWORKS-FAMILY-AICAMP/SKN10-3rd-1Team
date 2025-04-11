from langchain_chroma import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import time
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

def load_vector_store() -> Chroma:
    pdf_files = [
        "../data/2024년 하반기 3급 신입사원 채용 직무소개서.pdf",
        "../data/삼성전자 DS부문 24하 공채 직무기술서.pdf"
    ]
    docs = []
    for path in pdf_files:
        loader = PyPDFLoader(path)
        docs.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600, chunk_overlap=0)
    
    split_doc1 = text_splitter.split_documents(docs)

    # 저장할 경로 지정
    DB_PATH = "../../data/chroma_db"

    # 문서를 디스크에 저장합니다. 저장시 persist_directory에 저장할 경로를 지정합니다.
    db = Chroma.from_documents(
        split_doc1, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="my_db"
    )

    return db

def search_similarity(self_instruction:str, vector_store:Chroma, k:int=3) -> str:
    """Search for similar documents in the vector store."""
    return vector_store.similarity_search(self_instruction, k=k)[0].page_content

def get_prompt_template() -> PromptTemplate:
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

def get_answer(ollama:ChatOllama, context:str, self_instruction:str, query:str, prompt=get_prompt_template()) :
    """Get the answer from the chat model."""
    chain = prompt | ollama | StrOutputParser()
    for token in chain.stream({"context": context, "self_instruction": self_instruction, "query": query}):
        yield token
        time.sleep(0.05) 


