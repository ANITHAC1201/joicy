import streamlit as st
from auth import authenticate_user, register_user, login_user_session, logout_user_session, current_user
from ui import render_top_nav

# Top navigation
render_top_nav()

st.markdown('<h2 class="section-header">🔐 Login / Register</h2>', unsafe_allow_html=True)
st.caption("Access your workspace to upload media, run AI analysis, and manage results.")
st.divider()

# If already logged in, show status and logout option
user = current_user()
if user:
    with st.container():
        st.success(f"You are logged in as @{user['username']} · {user['email']}")
        col_acc_1, col_acc_2 = st.columns([1, 2])
        with col_acc_1:
            if st.button("Go to Home", use_container_width=True):
                st.switch_page("app.py")
        with col_acc_2:
            if st.button("Logout", use_container_width=True):
                logout_user_session()
                st.toast("Logged out")
                st.rerun()
else:
    tabs = st.tabs(["Login", "Register"])

    with tabs[0]:
        st.subheader("Login")
        st.write("Use your username or email to sign in.")
        with st.form("login_form", enter_to_submit=True, border=True):
            username_or_email = st.text_input("Username or Email", placeholder="e.g. johndoe or john@company.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            col_l_1, col_l_2 = st.columns([1, 2])
            with col_l_1:
                submit = st.form_submit_button("Login", type="primary", use_container_width=True)
            with col_l_2:
                st.caption("Tip: You can register in the next tab if you don't have an account.")
        if submit:
            ok, msg, user_obj = authenticate_user(username_or_email.strip(), password)
            if ok:
                login_user_session(user_obj)
                st.success("Login successful")
                st.rerun()
            else:
                st.error(msg)

    with tabs[1]:
        st.subheader("Register")
        st.write("Create your account to access all features.")
        with st.form("register_form", enter_to_submit=True, border=True):
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Username", placeholder="johndoe", help="Unique, 3-20 characters")
            with col2:
                email = st.text_input("Email", placeholder="john@company.com")
            colp1, colp2 = st.columns(2)
            with colp1:
                password = st.text_input("Password", type="password", placeholder="Minimum 8 characters")
            with colp2:
                confirm = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
            st.caption("By creating an account you agree to our terms of service.")
            submit_reg = st.form_submit_button("Create Account", type="primary", use_container_width=True)
        if submit_reg:
            if not username or not email or not password:
                st.error("Please fill in all fields")
            elif len(username) < 3 or len(username) > 20:
                st.error("Username must be 3-20 characters")
            elif password != confirm:
                st.error("Passwords do not match")
            else:
                ok, msg = register_user(username.strip(), email.strip(), password)
                if ok:
                    st.success("Registration successful. You can now login.")
                else:
                    st.error(msg)
