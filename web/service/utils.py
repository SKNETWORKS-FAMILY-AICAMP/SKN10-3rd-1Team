import streamlit as st
from service.history import add_history
from service.display import print_message
from service.constant import ROLE_TYPE
 

def init_button_session() : 
    if "profile_clicked" not in st.session_state:
        st.session_state.profile_clicked = False

    if "posting_clicked" not in st.session_state:
        st.session_state.posting_clicked = False

def handle_message(role:ROLE_TYPE, messages, msg_type) :
    add_history(role, 
            messages, msg_type)
    print_message(role.name, messages)