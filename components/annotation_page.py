import streamlit as st
from ui import render_top_nav

def show_annotation_page():
    st.markdown('<h2 class="section-header">✍️ Annotation Tool</h2>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="background: var(--card-background); border: 1px solid var(--border-color); border-radius: var(--border-radius); padding: 2rem; text-align: center; margin: 2rem 0;">
            <h3>🚧 Coming Soon</h3>
            <p>The annotation tool is currently under development. This feature will allow you to:</p>
            <ul style="text-align: left; max-width: 500px; margin: 1rem auto;">
                <li>📝 Manually annotate detected issues</li>
                <li>🏷️ Add custom labels and tags</li>
                <li>📊 Create detailed inspection reports</li>
                <li>✅ Validate AI predictions</li>
                <li>📋 Export annotated datasets</li>
            </ul>
            <p><strong>Expected Release:</strong> Next Update</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.info("💡 Use the sidebar navigation to access other features like Upload, Analysis, and Admin Panel.")

# Note: This function should only be called from the main app router, not at module level
