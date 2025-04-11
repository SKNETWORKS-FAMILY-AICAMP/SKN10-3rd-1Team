import enum
import time
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from service.constant import ROLE_TYPE, HISTORY_INFO

def make_ai_response(model_name, messages)  : 
    llm = ChatOllama(model=model_name)
    messages = messages
    prompts = []
    for msg in messages[:-1]: # 사용자의 메세지는 제외
      prompts.append(tuple(msg.values()))
    
    prompts += [(ROLE_TYPE.user.name, "{user_input}")] # 사용자의 메세지 입력 프론프트
    chat_prompt = ChatPromptTemplate.from_messages(prompts)

    # 체인 생성
    chain = chat_prompt | llm | StrOutputParser()
    # 모델 답변 
    return chain.stream({"user_input": messages[-1][HISTORY_INFO.content.name]})