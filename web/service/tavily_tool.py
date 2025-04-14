import requests
from openai import OpenAI
from langchain.tools import Tool
import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from LLM.llm import get_prompt_template
from langchain_core.output_parsers import StrOutputParser
import time

# 🔍 Tavily 검색
def tavily_search(query: str, tavily_key) -> str:
    url = "https://api.tavily.com/search"
    headers = {
        "Authorization": f"Bearer {tavily_key}",
        "Content-Type": "application/json"
    }
    data = {
        "query": query,
        "search_depth": "advanced",
        "include_answer": True,
        "max_results": 5,
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return f"Tavily 검색 오류: {response.status_code} - {response.text}"


# 🧠 전체 통합
def tavily_search_korean(query: str, tavily_key, openai_key, llm) -> str:
    context = tavily_search(query, tavily_key=tavily_key)
    prompt_template = get_prompt_template(tavily=True)
    chain = prompt_template | llm | StrOutputParser()
    return chain.invoke({"context": context, "query": query})
