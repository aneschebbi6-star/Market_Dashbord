import streamlit as st
from views.login import render_login_page

def check_password():
    """Returns `True` if the user had a correct password."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    submitted, user, pwd = render_login_page()
    
    if submitted:
        if user == "Anes0123" and pwd == "chebbi@1":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            # Re-render the error message from the view component
            st.error("⛔ Accès refusé — Identifiants invalides")

    return False
