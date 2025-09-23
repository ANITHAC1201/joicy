import streamlit as st
from auth import current_user

def render_sidebar_navigation():
    """Render a clean, organized sidebar navigation"""
    
    # Enhanced sidebar styling
    st.markdown(
        """
        <style>
        
        .sidebar-nav {
            padding: 1rem 0;
        }
        
        .nav-section {
            margin-bottom: 2rem;
        }
        
        .nav-section-title {
            font-size: 0.875rem;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.75rem;
            padding: 0 1rem;
        }
        
        .nav-item {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem 1rem;
            margin: 0.25rem 0.5rem;
            border-radius: var(--border-radius-sm);
            color: var(--text-secondary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.2s ease;
            cursor: pointer;
        }
        
        .nav-item:hover {
            background: var(--card-background);
            color: var(--text-primary);
            transform: translateX(4px);
        }
        
        .nav-item.active {
            background: var(--primary-color);
            color: white;
            font-weight: 600;
        }
        
        .nav-icon {
            font-size: 1.25rem;
            width: 1.5rem;
            text-align: center;
        }
        
        .nav-badge {
            background: var(--error-color);
            color: white;
            font-size: 0.75rem;
            padding: 0.125rem 0.375rem;
            border-radius: 999px;
            margin-left: auto;
        }
        
        .nav-divider {
            height: 1px;
            background: var(--border-color);
            margin: 1rem 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Get current user for admin check
    user = current_user()
    is_admin = user and user['username'].lower() in ["admin", "administrator"]
    
    # Navigation structure
    st.sidebar.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
    
    # Main Navigation Section
    st.sidebar.markdown('<div class="nav-section-title">📊 Dashboard</div>', unsafe_allow_html=True)
    
    if st.sidebar.button("🏠 Home Dashboard", key="nav_home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    
    st.sidebar.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)
    
    # Workflow Section
    st.sidebar.markdown('<div class="nav-section-title">🔄 Workflow</div>', unsafe_allow_html=True)
    
    if st.sidebar.button("📤 Media Upload", key="nav_upload", use_container_width=True):
        st.session_state.page = "upload"
        st.rerun()
    
    if st.sidebar.button("🤖 AI Analysis", key="nav_analysis", use_container_width=True):
        st.session_state.page = "analysis"
        st.rerun()
    
    if st.sidebar.button("✍️ Annotation Tool", key="nav_annotation", use_container_width=True):
        st.session_state.page = "annotation"
        st.rerun()
    
    # Admin Section (only for admin users)
    if is_admin:
        st.sidebar.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)
        st.sidebar.markdown('<div class="nav-section-title">🛡️ Administration</div>', unsafe_allow_html=True)
        
        if st.sidebar.button("🛡️ Admin Panel", key="nav_admin_sidebar", use_container_width=True):
            st.session_state.page = "admin"
            st.rerun()
    
    st.sidebar.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)
    
    # User Status Section
    if user:
        st.sidebar.markdown('<div class="nav-section-title">👤 Account</div>', unsafe_allow_html=True)
        st.sidebar.success(f"Logged in as @{user['username']}")
        st.sidebar.caption(f"📧 {user['email']}")
        
        if is_admin:
            st.sidebar.info("🛡️ Admin Access Enabled")
    else:
        st.sidebar.markdown('<div class="nav-section-title">🔐 Authentication</div>', unsafe_allow_html=True)
        st.sidebar.warning("Please log in to access features")
        
        if st.sidebar.button("🔐 Login / Register", key="nav_login_sidebar", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()
    
    # Help Section
    st.sidebar.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="nav-section-title">❓ Support</div>', unsafe_allow_html=True)
    
    with st.sidebar.expander("📚 Quick Help"):
        st.markdown("""
        **Getting Started:**
        1. 🔐 Login/Register first
        2. 📤 Upload drone media
        3. 🤖 Run AI analysis
        4. ✍️ Review & annotate
        
        **Need Help?**
        - Check the "How to Use" tab
        - Contact support team
        """)
    
    with st.sidebar.expander("ℹ️ App Info"):
        st.markdown("""
        **FLYSCOPE v2.0**
        - Infrastructure AI Platform
        - Drone-based Inspection
        - Real-time Analysis
        
        **Status:** ✅ Online
        """)
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
