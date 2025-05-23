import streamlit as st
from service.constant import HISTORY_INFO, MODEL, ROLE_TYPE
# 히스토리 초기화 
def init_history():
  if "messages" not in st.session_state: # session_state에 messages라는 키가 없다면, 
    # messages 이름으로 리스트 데이터 기억하기!
    st.session_state.messages = [] # 초기화!!! 


# 사용자 & AI message 추가 
def add_history(role:ROLE_TYPE, message, function):
  # isinstance(변수, 타입) -> 변수의 타입이 타입과 같으면, True / 아니면, False
  if not isinstance(role, ROLE_TYPE):
    raise Exception("히스토리에 추가하지 않음")

  st.session_state.messages.append({
    HISTORY_INFO.role.name: role.name, 
    HISTORY_INFO.content.name: message,
    HISTORY_INFO.function.name : function
  })