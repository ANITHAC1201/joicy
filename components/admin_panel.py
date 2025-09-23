import streamlit as st
import sqlite3
from datetime import datetime
from auth import require_login, current_user, get_conn
from ui import render_top_nav

# Get all users from database
def get_all_users():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email, created_at FROM users ORDER BY created_at DESC")
    users = cur.fetchall()
    conn.close()
    return users

# Delete user function
def delete_user(user_id, username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return cur.rowcount > 0

# Get user statistics
def get_user_stats():
    conn = get_conn()
    cur = conn.cursor()
    
    # Total users
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]
    
    # Users registered today
    today = datetime.now().date().isoformat()
    cur.execute("SELECT COUNT(*) FROM users WHERE DATE(created_at) = ?", (today,))
    today_users = cur.fetchone()[0]
    
    # Users registered this week
    cur.execute("SELECT COUNT(*) FROM users WHERE created_at >= date('now', '-7 days')")
    week_users = cur.fetchone()[0]
    
    conn.close()
    return total_users, today_users, week_users

# Enhanced admin styling
st.markdown(
    """
    <style>
    .admin-header {
        background: linear-gradient(135deg, var(--error-color), #dc2626);
        color: white;
        padding: 1.5rem;
        border-radius: var(--border-radius);
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-lg);
    }
    
    .admin-title {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .user-card {
        background: var(--card-background);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow);
        transition: all 0.2s ease;
    }
    
    .user-card:hover {
        border-color: var(--primary-color);
        box-shadow: var(--shadow-lg);
    }
    
    .user-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .user-details {
        flex: 1;
    }
    
    .user-name {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }
    
    .user-email {
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-bottom: 0.25rem;
    }
    
    .user-date {
        color: var(--text-muted);
        font-size: 0.8rem;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .stat-card {
        background: var(--card-background);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        text-align: center;
        box-shadow: var(--shadow);
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 800;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: var(--text-secondary);
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .danger-zone {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid var(--error-color);
        border-radius: var(--border-radius);
        padding: 1rem;
        margin-top: 1rem;
    }
    
    .warning-text {
        color: var(--error-color);
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def show_admin_panel():
    # Admin panel header
    st.markdown(
        """
        <div class="admin-header">
            <div class="admin-title">🛡️ Admin Panel</div>
            <p>User Management & System Administration</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Require login
    require_login()
    user = current_user()

    # Simple admin check (you can enhance this with a proper admin role system)
    ADMIN_USERS = ["admin", "administrator"]  # Add your admin usernames here
    is_admin = user and user['username'].lower() in ADMIN_USERS

    if not is_admin:
        st.error("🚫 Access Denied: Admin privileges required")
        st.info("Contact your system administrator to request admin access.")
        st.stop()

    st.success(f"Welcome, Admin @{user['username']}!")

    # Display statistics
    total_users, today_users, week_users = get_user_stats()

    st.markdown("### 📊 User Statistics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-value">{total_users}</div>
                <div class="stat-label">Total Users</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-value">{today_users}</div>
                <div class="stat-label">Registered Today</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-value">{week_users}</div>
                <div class="stat-label">This Week</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # User management section
    st.markdown("### 👥 User Management")

    # Search and filter options
    search_col, filter_col = st.columns([2, 1])
    with search_col:
        search_term = st.text_input("🔍 Search users", placeholder="Search by username or email...")
    with filter_col:
        sort_option = st.selectbox("Sort by", ["Newest First", "Oldest First", "Username A-Z", "Username Z-A"])

    # Get and display users
    users = get_all_users()

    # Apply search filter
    if search_term:
        users = [u for u in users if search_term.lower() in u[1].lower() or search_term.lower() in u[2].lower()]

    # Apply sorting
    if sort_option == "Oldest First":
        users = users[::-1]
    elif sort_option == "Username A-Z":
        users = sorted(users, key=lambda x: x[1].lower())
    elif sort_option == "Username Z-A":
        users = sorted(users, key=lambda x: x[1].lower(), reverse=True)

    if users:
        st.markdown(f"**Found {len(users)} user(s)**")
        
        for user_data in users:
            user_id, username, email, created_at = user_data
            
            # Parse creation date
            try:
                created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                formatted_date = created_date.strftime("%B %d, %Y at %I:%M %p")
            except:
                formatted_date = created_at
            
            # User card
            with st.container():
                st.markdown(
                    f"""
                    <div class="user-card">
                        <div class="user-info">
                            <div class="user-details">
                                <div class="user-name">👤 {username}</div>
                                <div class="user-email">📧 {email}</div>
                                <div class="user-date">📅 Joined: {formatted_date}</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Action buttons
                col_actions1, col_actions2, col_actions3 = st.columns([1, 1, 2])
                
                with col_actions1:
                    if st.button(f"📝 Edit", key=f"edit_{user_id}"):
                        st.info("Edit functionality coming soon!")
                
                with col_actions2:
                    if st.button(f"📊 Activity", key=f"activity_{user_id}"):
                        st.info("Activity logs coming soon!")
                
                with col_actions3:
                    # Danger zone for delete
                    with st.expander("🗑️ Delete User", expanded=False):
                        st.markdown(
                            f"""
                            <div class="danger-zone">
                                <div class="warning-text">⚠️ Danger Zone</div>
                                <p>This action cannot be undone. The user <strong>{username}</strong> will be permanently deleted.</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
                        # Confirmation checkbox
                        confirm_delete = st.checkbox(
                            f"I understand this will permanently delete {username}",
                            key=f"confirm_{user_id}"
                        )
                        
                        if confirm_delete:
                            if st.button(
                                f"🗑️ DELETE {username}",
                                key=f"delete_{user_id}",
                                type="primary",
                                use_container_width=True
                            ):
                                if delete_user(user_id, username):
                                    st.success(f"✅ User {username} has been deleted successfully!")
                                    st.balloons()
                                    st.rerun()
                                else:
                                    st.error(f"❌ Failed to delete user {username}")
                
                st.markdown("---")
    else:
        st.info("No users found matching your search criteria.")

    # Refresh button
    st.markdown("### 🔄 Actions")
    if st.button("🔄 Refresh User List", use_container_width=True):
        st.rerun()

    # Additional admin tools
    with st.expander("🛠️ Additional Admin Tools"):
        st.markdown("**Database Information**")
        st.code(f"Database Path: {get_conn().execute('PRAGMA database_list').fetchall()}")
        
        if st.button("📊 Export User Data"):
            st.info("Export functionality coming soon!")
        
        if st.button("🧹 Database Cleanup"):
            st.info("Cleanup functionality coming soon!")
