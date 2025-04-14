import streamlit as st
from service.constant import  ROLE_TYPE, FUNC_TYPE
from service.display import print_message, print_history_message
from service.history import init_history
from service.utils import handle_message, is_txt_file
from service.input import get_prompt
from LLM.llm import load_vector_store, search_similarity, get_answer
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from service.tavily_tool import tavily_search_korean
from langchain.tools import Tool
import os

st.title("삼성전자 취업 컨설팅 챗봇")

load_dotenv()
init_history()
vector_db = load_vector_store() 
llm = ChatGroq(model="gemma2-9b-it")

# api 키 설정
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# 선택지 정의
option = st.selectbox(
    "기능을 선택하세요 👇",
    ["자소서 피드백", "구인의뢰 검색"]
)

# 조건 분기
if option == "자소서 피드백":
    print_message(ROLE_TYPE.assistant.name,"안녕하세요! 삼성전자 취업 컨설팅 챗봇입니다.")
    print_message(ROLE_TYPE.assistant.name,"📜 자소서 피드백 페이지입니다. \
                    자소서 파일을 올려주시고, 원하시는 질문을 입력하세요!")
    prompt = get_prompt(is_file=True)
    if prompt is not None : 
        # 사용자 입력/ 자소서 질문, 답변을 구분짓기 위해 msg_type을 추가함.
        # accept_file이 있기 때문에 chatinputValue 객체가 되니 .text를 붙여야됨.
        print_history_message(FUNC_TYPE.cover_letter.name)
        handle_message(ROLE_TYPE.user, prompt.text, FUNC_TYPE.cover_letter.name)
        if not prompt.files : 
            handle_message(ROLE_TYPE.assistant, 
            "🚨 오류 : 파일을 입력해주세요!!",FUNC_TYPE.cover_letter.name,is_streaming=True)
        else : 
            file = is_txt_file(prompt.files[0])
            messages = file.read().decode("utf-8")
            context = search_similarity(messages, vector_db)
            response =  get_answer(llm, context, messages, prompt.text)
            handle_message(ROLE_TYPE.assistant,response,FUNC_TYPE.cover_letter.name, is_streaming=True)
            
elif option == "구인의뢰 검색":
    print_message(ROLE_TYPE.assistant.name,"안녕하세요! 삼성전자 취업 컨설팅 챗봇입니다.")
    print_message(ROLE_TYPE.assistant.name,
    "🏢 구인의뢰 검색 페이지입니다. 삼성전자 채용, 뉴스, 트렌드 관련 질문에 사용해주세요~")
    prompt = get_prompt(is_file=False)
    if prompt is not None : 
        print_history_message(FUNC_TYPE.job_search.name)
        handle_message(ROLE_TYPE.user, prompt,FUNC_TYPE.job_search.name)

        # ✅ LangChain Tool 객체 생성
        tavily_tool = Tool(
            name="TavilySearchKorean",
            func=tavily_search_korean,
            description=(
                "실시간 웹 검색 결과를 한글로 요약해주는 도구입니다. "
                "삼성전자 채용, 뉴스, 트렌드 관련 질문에 사용하세요."
            )
        )
        result = tavily_search_korean(prompt, tavily_key=TAVILY_API_KEY, openai_key=OPENAI_API_KEY, llm=llm)
        handle_message(ROLE_TYPE.assistant, "🔍 최종 검색 결과 (한국어): " + result, FUNC_TYPE.job_search.name ,is_streaming=True)
    





