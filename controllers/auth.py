import os
from pathlib import Path

import streamlit as st
from streamlit.runtime.secrets import StreamlitSecretNotFoundError
from views.login import render_login_page

try:
    from dotenv import load_dotenv
    project_root = Path(__file__).resolve().parent.parent
    dotenv_path = project_root / ".env"
    if dotenv_path.exists():
        load_dotenv(dotenv_path=dotenv_path)
    else:
        load_dotenv()
except ImportError:
    pass


def load_auth_credentials():
    """Load login credentials from environment variables or Streamlit secrets."""
    username = os.getenv("DASHBOARD_USER") or os.getenv("dashboard_user")
    password = os.getenv("DASHBOARD_PASSWORD") or os.getenv("dashboard_password")

    if username:
        username = username.strip()
    if password:
        password = password.strip()

    if not username or not password:
        try:
            username = st.secrets.get("user")
            password = st.secrets.get("password")
        except StreamlitSecretNotFoundError:
            username = username or None
            password = password or None

    return username, password


def check_password():
    """Returns `True` if the user had a correct password."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    submitted, user, pwd = render_login_page()
    
    if submitted:
        expected_user, expected_pwd = load_auth_credentials()

        if not expected_user or not expected_pwd:
            st.error(
                "⛔ Aucun identifiant configuré. Définissez `DASHBOARD_USER`/`DASHBOARD_PASSWORD` ou utilisez `st.secrets`."
            )
            return False

        if user == expected_user and pwd == expected_pwd:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("⛔ Accès refusé — Identifiants invalides")

    return False
