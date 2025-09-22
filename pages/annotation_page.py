import streamlit as st
def show_annotation_page():
    st.markdown('<h2 class="section-header">✍️ Annotation Tool (Disabled)</h2>', unsafe_allow_html=True)
    st.info("The annotation tool is currently disabled as requested. You can re-enable it later.")
    st.write("Use the sidebar to navigate to other features like Upload, Analysis, Results, and Mapping.")

# Render a simple informational page to avoid errors in multipage mode
show_annotation_page()
