import streamlit as st
from service.constant import HISTORY_INFO, MODEL, ROLE_TYPE, MSG_TYPE
from service.display import print_message, print_history_message, generate_msg
from service.history import init_history, add_history
from service.utils import init_button_session, handle_message, is_txt_file
from service.input import get_prompt
st.title("삼성전자 취업 컨설팅 챗봇")

# 모델 선택 selectbox
col1, col2 = st.columns([1,4])  # 2개의 열로 분할
with col1:
    choice_model = st.selectbox(label="모델",options=MODEL.__members__)

print_message(ROLE_TYPE.assistant.name,
              "안녕하세요! 삼성전자 취업 컨설팅 챗봇입니다. \
              원하시는 메뉴를 선택하세요!")

init_history()
print_history_message()
init_button_session()
    
if st.session_state.profile_clicked == False and st.session_state.posting_clicked == False :
    if st.button("📜 자소서 피드백"):
        st.session_state.profile_clicked = True
        add_history(ROLE_TYPE.assistant,"자소서 피드백을 선택하셨습니다. \
                    자소서 파일을 올려주시고, 원하시는 질문을 입력하세요!",
                    MSG_TYPE.system.name)
        st.rerun() # rerun() : 전체 재실행, 단 session은 그대로 남아있음.
        
    if st.button("🏢 구인의뢰 검색"):
        st.session_state.posting_clicked = True
        add_history(ROLE_TYPE.assistant,
                    "구인의뢰 검색을 선택하셨습니다.",
                    MSG_TYPE.system.name)
        st.rerun() # rerun() : 전체 재실행, 단 session은 그대로 남아있음.

elif st.session_state.profile_clicked == True : 
    prompt = get_prompt(is_file=True)
    if prompt is not None : 
        # 사용자 입력/ 자소서 질문, 답변을 구분짓기 위해 msg_type을 추가함.
        # accept_file이 있기 때문에 chatinputValue 객체가 되니 .text를 붙여야됨.
        handle_message(ROLE_TYPE.user, prompt.text, MSG_TYPE.user.name)
        if not prompt.files : 
            handle_message(ROLE_TYPE.assistant, 
            "🚨 오류 : 파일을 입력해주세요!!", MSG_TYPE.system.name, is_streaming=True)
        else : 
            file = is_txt_file(prompt.files[0])
            st.write(file.name)


elif st.session_state.posting_clicked == True :
    prompt = get_prompt(is_file=False)
    if prompt is not None : 
        handle_message(ROLE_TYPE.user, prompt, MSG_TYPE.user.name)



