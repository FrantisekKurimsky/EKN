"""Authentication utilities for protected pages."""
import streamlit as st
import hmac


def require_login_for_protected_pages() -> bool:
    """Check if user is authenticated for protected pages."""
    auth_config = st.secrets.get("auth")
    if not auth_config or not auth_config.get("password"):
        st.error("Prihlasovanie nie je nastavene. Doplňte [auth] password do .streamlit/secrets.toml.")
        return False

    expected_password = str(auth_config["password"])
    if "is_authenticated" not in st.session_state:
        st.session_state.is_authenticated = False

    if st.session_state.is_authenticated:
        return True

    st.subheader("Prihlásenie")
    with st.form("protected_login_form"):
        password = st.text_input("Heslo", type="password")
        submitted = st.form_submit_button("Prihlásiť")

    if submitted:
        if hmac.compare_digest(password, expected_password):
            st.session_state.is_authenticated = True
            st.success("Prihlásenie úspešné.")
            st.rerun()
        else:
            st.error("Nesprávne heslo.")

    return False


def show_logout_button():
    """Display logout button in page header area if user is authenticated."""
    if st.session_state.get("is_authenticated"):
        col_left, col_right = st.columns([8, 1])
        with col_right:
            if st.button("Odhlásiť", key="logout_button"):
                st.session_state.is_authenticated = False
                st.rerun()
