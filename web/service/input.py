import streamlit as st


def get_prompt(is_file:bool) :
    if is_file : 
        return st.chat_input("입력해주세요.", accept_file=True)
    return st.chat_input("입력해주세요.")