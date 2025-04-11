import streamlit as st
from service.constant import HISTORY_INFO, MODEL, ROLE_TYPE
from service.display import print_message, print_history_message
from service.history import init_history, add_history
st.title("삼성전자 취업 컨설팅 챗봇")

# 모델 선택 selectbox
col1, col2 = st.columns([1,4])  # 2개의 열로 분할
with col1:
    choice_model = st.selectbox(label="모델",options=MODEL.__members__)

print_message(ROLE_TYPE.assistant.name,"안녕하세요! 삼성전자 취업 컨설팅 챗봇입니다. \
              원하시는 메뉴를 선택하세요!")

init_history()
print_history_message()

if "profile_clicked" not in st.session_state:
    st.session_state.profile_clicked = False

if "posting_clicked" not in st.session_state:
    st.session_state.posting_clicked = False
    
if st.session_state.profile_clicked == False and st.session_state.posting_clicked == False :
    if st.button("📜 자소서 피드백"):
        st.session_state.profile_clicked = True
        add_history(ROLE_TYPE.assistant,"자소서 피드백을 선택하셨습니다. 자소서 파일을 올려주시고, 원하시는 질문을 입력하세요!")
        st.rerun() # rerun() : 전체 재실행, 단 session은 그대로 남아있음.
    if st.button("🏢 구인의뢰 검색"):
        st.session_state.posting_clicked = True
        add_history(ROLE_TYPE.assistant,"구인의뢰 검색을 선택하셨습니다.")
        st.rerun() # rerun() : 전체 재실행, 단 session은 그대로 남아있음.

else : 
    st.chat_input("입력해주세요.", accept_file=True)
#if st.button("📜 자소서 피드백"):
#    st.markdown("자소서 피드백을 선택하셨습니다. 파일을 업로드하고, 원하는 피드백을 말해주세요!")
#    st.button("처음으로")
#elif st.button("🏢 구인의뢰 검색"):
#    st.markdown("구인의뢰 검색을 선택하셨습니다. 원하시는 회사를 말씀해주세요!")
#    st.button("처음으로")

