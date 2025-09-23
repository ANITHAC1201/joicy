import streamlit as st
from auth import authenticate_user, register_user, login_user_session, logout_user_session, current_user
from ui import render_top_nav

# Enhanced page config for login
st.markdown(
    """
    <style>
    .login-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem 0;
    }
    
    .auth-card {
        background: var(--card-background);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        padding: 2rem;
        box-shadow: var(--shadow-lg);
        margin-bottom: 2rem;
    }
    
    .auth-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .auth-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary-color), #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .auth-subtitle {
        color: var(--text-secondary);
        font-size: 1.1rem;
        margin-bottom: 0;
    }
    
    .success-card {
        background: linear-gradient(135deg, var(--success-color), #059669);
        color: white;
        border-radius: var(--border-radius);
        padding: 2rem;
        text-align: center;
        box-shadow: var(--shadow-lg);
    }
    
    .form-section {
        margin-bottom: 1.5rem;
    }
    
    .form-label {
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .helper-text {
        color: var(--text-muted);
        font-size: 0.875rem;
        margin-top: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def show_login_page():
    # Enhanced header section
    st.markdown(
        """
        <div class="login-container">
            <div class="auth-header">
                <h1 class="auth-title">🔐 Authentication</h1>
                <p class="auth-subtitle">Access your workspace to upload media, run AI analysis, and manage results</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Enhanced logged-in user section
    user = current_user()
    if user:
        st.markdown(
            f"""
            <div class="success-card">
                <h3>✅ Welcome back, {user['username']}!</h3>
                <p>You are successfully logged in as <strong>{user['email']}</strong></p>
                <p>You now have access to all platform features including media upload, AI analysis, and reporting.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
        
        col_home, col_logout = st.columns([1, 1])
        with col_home:
            if st.button("🏠 Go to Dashboard", key="login_go_home_btn", use_container_width=True):
                st.session_state.page = "home"
                st.rerun()
        with col_logout:
            if st.button("🚪 Logout", key="login_page_logout_btn", use_container_width=True):
                logout_user_session()
                st.toast("Successfully logged out!")
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
                    submit = st.form_submit_button("Login", type="primary", use_container_width=True, key="login_form_submit_btn")
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
                submit_reg = st.form_submit_button("Create Account", type="primary", use_container_width=True, key="register_form_submit_btn")
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
