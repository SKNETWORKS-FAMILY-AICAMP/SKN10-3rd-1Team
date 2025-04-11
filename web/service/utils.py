import streamlit as st
from service.history import add_history
from service.display import print_message, generate_msg
from service.constant import ROLE_TYPE
import re
 

def init_button_session() : 
    if "profile_clicked" not in st.session_state:
        st.session_state.profile_clicked = False

    if "posting_clicked" not in st.session_state:
        st.session_state.posting_clicked = False

def handle_message(role:ROLE_TYPE, messages, msg_type, is_streaming=False) :
    add_history(role, 
            messages, msg_type)
    if is_streaming :
        print_message(role.name,generate_msg(messages))
    else : 
        print_message(role.name,messages)

def is_txt_file(file) :
    if not file.name.endswith(".txt") :
        st.write("🚨 오류 : 해당 파일은 텍스트(.txt)파일이 아닙니다!")
    else :
        return file