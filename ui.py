import streamlit as st
from auth import current_user, logout_user_session

def render_top_nav():
    # Enhanced top navigation styling
    st.markdown(
        """
        <style>
        .top-nav-container {
            background: linear-gradient(135deg, var(--card-background), var(--background-dark));
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            padding: 1rem 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: var(--shadow);
            backdrop-filter: blur(10px);
        }
        
        .brand-section {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .brand-logo {
            font-size: 1.5rem;
            background: linear-gradient(135deg, var(--primary-color), #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .brand-text {
            font-weight: 700;
            font-size: 1.25rem;
            color: var(--text-primary);
        }
        
        .brand-subtitle {
            color: var(--text-muted);
            font-size: 0.875rem;
            font-weight: 400;
        }
        
        .account-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 999px;
            background: var(--card-background);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            font-size: 0.875rem;
            font-weight: 500;
            box-shadow: var(--shadow);
            margin-bottom: 0.75rem;
        }
        
        .nav-buttons {
            display: flex;
            gap: 0.5rem;
        }
        
        .stButton > button {
            background: var(--card-background) !important;
            border: 1px solid var(--border-color) !important;
            color: var(--text-primary) !important;
            font-weight: 600 !important;
            padding: 0.5rem 1rem !important;
            border-radius: var(--border-radius-sm) !important;
            transition: all 0.2s ease !important;
        }
        
        .stButton > button:hover {
            background: var(--primary-color) !important;
            border-color: var(--primary-color) !important;
            transform: translateY(-1px) !important;
            box-shadow: var(--shadow) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Enhanced navigation container
    st.markdown('<div class="top-nav-container">', unsafe_allow_html=True)
    
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.markdown(
            """
            <div class="brand-section">
                <span class="brand-logo">🚁</span>
                <div>
                    <div class="brand-text">FLYSCOPE</div>
                    <div class="brand-subtitle">Infrastructure AI Platform</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col_right:
        user = current_user()
        if user:
            st.markdown(
                f"""
                <div class='account-chip'>
                    <span style="color: var(--success-color);">●</span>
                    <span>@{user['username']}</span>
                    <span style="color: var(--text-muted);">·</span>
                    <span style="color: var(--text-muted); font-size: 0.8rem;">{user['email']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
            # Simple logout button for logged-in users
            if st.button("🚪 Logout", key="nav_logout_btn", use_container_width=True):
                logout_user_session()
                st.rerun()
        else:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔐 Login / Register", key="nav_login_btn", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
