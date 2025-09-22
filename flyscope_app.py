import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import base64
import tempfile
import os
import random
from folium.plugins import MarkerCluster, HeatMap
import zipfile
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet

# All page functions are now included in this file

# Page configuration
st.set_page_config(
    page_title="FLYSCOPE - AI Drone Inspection",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_theme():
    theme = st.session_state.get('theme', 'Dark')
    if theme == 'Dark':
        css = """
        <style>
        .main {background: linear-gradient(180deg, #0f172a 0%, #111827 100%); color: #e5e7eb;}
        .block-container {padding-top: 2rem;}
        .main-header {font-size: 3rem; background: linear-gradient(90deg, #60a5fa, #34d399, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 0.25rem; font-weight: 800; letter-spacing: 1px;}
        .subheader-tagline {text-align: center; color: #94a3b8; margin-bottom: 2rem;}
        .section-header {font-size: 1.5rem; color: #cbd5e1; margin-top: 1.25rem; margin-bottom: 0.75rem; border-left: 4px solid #34d399; padding-left: .5rem;}
        div.stButton>button {background: linear-gradient(90deg, #2563eb, #34d399); color: white; border: 0; border-radius: 8px; padding: .5rem 1rem; font-weight: 600;}
        div.stButton>button:hover { filter: brightness(1.05); }
        section[data-testid="stSidebar"] {background: #0b1220; border-right: 1px solid #1f2937;}
        </style>
        """
    else:
        css = """
        <style>
        .main {background: #f8fafc; color: #0f172a;}
        .block-container {padding-top: 2rem;}
        .main-header {font-size: 3rem; background: linear-gradient(90deg, #3b82f6, #10b981, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 0.25rem; font-weight: 800; letter-spacing: 1px;}
        .subheader-tagline {text-align: center; color: #334155; margin-bottom: 2rem;}
        .section-header {font-size: 1.5rem; color: #0f172a; margin-top: 1.25rem; margin-bottom: 0.75rem; border-left: 4px solid #10b981; padding-left: .5rem;}
        div.stButton>button {background: linear-gradient(90deg, #2563eb, #10b981); color: white; border: 0; border-radius: 8px; padding: .5rem 1rem; font-weight: 600;}
        div.stButton>button:hover { filter: brightness(0.95); }
        section[data-testid="stSidebar"] {background: #ffffff; border-right: 1px solid #e5e7eb;}
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

def main():
    apply_theme()
    st.markdown('<h1 class="main-header">🚁 FLYSCOPE</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #7f8c8d;">AI-Powered Drone Inspection System for Safer Infrastructure Monitoring</p>', unsafe_allow_html=True)
    
    # Sidebar navigation with remembered selection
    NAV_PAGES = [
        "🏠 Home",
        "📤 Media Upload",
        "🤖 AI Analysis",
        "📊 Results & Reports",
        "🗺️ Fault Mapping",
        "📁 Data Management",
        "⚙️ Settings"
    ]
    st.sidebar.title("Navigation")
    default_page = st.session_state.get('nav', "🏠 Home")
    if default_page not in NAV_PAGES:
        default_page = "🏠 Home"
    page = st.sidebar.selectbox("Choose a page", NAV_PAGES, index=NAV_PAGES.index(default_page))
    st.session_state.nav = page
    
    if page == "🏠 Home":
        show_home_page()
    elif page == "📤 Media Upload":
        show_upload_page()
    elif page == "🤖 AI Analysis":
        show_analysis_page()
    elif page == "📊 Results & Reports":
        show_results_page()
    elif page == "🗺️ Fault Mapping":
        show_mapping_page()
    elif page == "📁 Data Management":
        show_data_management_page()
    elif page == "⚙️ Settings":
        show_settings_page()

def show_home_page():
    st.markdown('<h2 class="section-header">Welcome to FLYSCOPE</h2>', unsafe_allow_html=True)
    
    # KPI metrics
    k1, k2, k3, k4 = st.columns(4)
    total_uploads = len(st.session_state.get('uploaded_media', []))
    total_results = len(st.session_state.get('analysis_results', []))
    total_detections = sum(len(r['detections']) for r in st.session_state.get('analysis_results', []))
    critical = sum(1 for r in st.session_state.get('analysis_results', []) for d in r['detections'] if d.get('severity') == 'Critical')
    with k1: st.metric("Uploads", total_uploads)
    with k2: st.metric("Analyses", total_results)
    with k3: st.metric("Detections", total_detections)
    with k4: st.metric("Critical", critical)

    col1, col2 = st.columns([2,1])
    
    with col1:
        st.markdown("""
        ### 🎯 Project Goals
        - Enhance infrastructure inspection safety and efficiency
        - Use affordable drones with real-time AI defect detection
        - Reduce human risk in dangerous inspection areas
        - Provide accurate, automated fault detection
        """)
        
        st.markdown("""
        ### 🔧 Core Features
        - **Image/Video Capture**: Manual or semi-autonomous drone operation
        - **AI-Powered Analysis**: Real-time crack and fault detection
        - **Visualization**: Bounding boxes, alerts, and heatmaps
        - **Data Storage**: Comprehensive reporting and scalability
        """)
    
    with col2:
        st.markdown("""
        ### 🛠️ Technologies Used
        - **Python**: Core programming language
        - **TensorFlow/PyTorch**: Deep learning frameworks
        - **OpenCV**: Computer vision processing
        - **Streamlit**: Web application framework
        - **Folium**: Interactive mapping
        """)
        
        st.markdown("""
        ### 📋 Workflow Steps
        1. Upload or capture drone media
        2. Select AI detection model
        3. Run automated inspection
        4. View results and generate reports
        5. Map detected faults geographically
        """)

    # Quick actions
    st.markdown('<h3 class="section-header">⚡ Quick Actions</h3>', unsafe_allow_html=True)
    qa1, qa2, qa3 = st.columns(3)
    with qa1:
        if st.button("📤 Go to Upload"):
            st.session_state.nav = "📤 Media Upload"
            st.rerun()
    with qa2:
        if st.button("🤖 Run Analysis"):
            st.session_state.nav = "🤖 AI Analysis"
            st.rerun()
    with qa3:
        if st.button("🗺️ View Map"):
            st.session_state.nav = "🗺️ Fault Mapping"
            st.rerun()

    # Recent gallery
    recent = [m for m in st.session_state.get('uploaded_media', []) if str(m['type']).startswith('image')][:6]
    if recent:
        st.markdown('<h3 class="section-header">🖼️ Recent Uploads</h3>', unsafe_allow_html=True)
        rows = [recent[i:i+3] for i in range(0, len(recent), 3)]
        for row in rows:
            c = st.columns(3)
            for idx, item in enumerate(row):
                with c[idx]:
                    try:
                        img = Image.open(item['path'])
                        st.image(img, caption=item['name'], use_column_width=True)
                    except Exception:
                        st.write(item['name'])

def show_upload_page():
    st.markdown('<h2 class="section-header">📤 Media Upload</h2>', unsafe_allow_html=True)
    
    # Upload options
    upload_option = st.radio(
        "Choose upload method:",
        ["Upload Files", "Live Drone Camera", "Sample Images"]
    )
    
    if upload_option == "Upload Files":
        handle_file_upload()
    elif upload_option == "Live Drone Camera":
        handle_live_camera()
    elif upload_option == "Sample Images":
        handle_sample_images()

def handle_file_upload():
    st.subheader("Upload Drone Images or Videos")
    
    uploaded_files = st.file_uploader(
        "Choose files",
        type=['jpg', 'jpeg', 'png', 'mp4', 'avi', 'mov'],
        accept_multiple_files=True,
        help="Supported formats: JPG, PNG, MP4, AVI, MOV"
    )
    
    if uploaded_files:
        st.success(f"Uploaded {len(uploaded_files)} file(s)")
        
        # Store uploaded files in session state
        if 'uploaded_media' not in st.session_state:
            st.session_state.uploaded_media = []
        
        for uploaded_file in uploaded_files:
            # Save file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                file_path = tmp_file.name
            
            file_info = {
                'name': uploaded_file.name,
                'path': file_path,
                'type': uploaded_file.type,
                'size': uploaded_file.size
            }
            
            if file_info not in st.session_state.uploaded_media:
                st.session_state.uploaded_media.append(file_info)
        
        # Display uploaded files
        display_uploaded_files()

def handle_sample_images():
    st.subheader("Sample Infrastructure Images")
    
    # Create sample images for demonstration
    sample_images = {
        "Bridge Crack": "bridge_crack",
        "Power Line Corrosion": "power_line", 
        "Building Damage": "building",
        "Road Surface": "road"
    }
    
    selected_samples = st.multiselect(
        "Select sample images to analyze:",
        list(sample_images.keys())
    )
    
    if selected_samples:
        if 'uploaded_media' not in st.session_state:
            st.session_state.uploaded_media = []
        
        for sample_name in selected_samples:
            # Create sample image
            img = create_sample_image(sample_images[sample_name])
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                img.save(tmp_file.name)
                
                file_info = {
                    'name': f"{sample_name.lower().replace(' ', '_')}.jpg",
                    'path': tmp_file.name,
                    'type': 'image/jpeg',
                    'size': os.path.getsize(tmp_file.name)
                }
                
                if file_info not in st.session_state.uploaded_media:
                    st.session_state.uploaded_media.append(file_info)
        
        st.success(f"Added {len(selected_samples)} sample image(s)")
        display_uploaded_files()

def handle_live_camera():
    st.subheader("Live Drone Camera Connection")
    st.info("🚧 Live camera integration coming soon!")
    
    drone_type = st.selectbox(
        "Select Drone Type:",
        ["DJI Tello", "DJI Mini", "Custom Drone", "Simulator"]
    )
    
    if drone_type == "Simulator":
        st.warning("Using camera simulator mode")

def display_uploaded_files():
    if 'uploaded_media' in st.session_state and st.session_state.uploaded_media:
        st.subheader("Uploaded Files")
        
        for i, file_info in enumerate(st.session_state.uploaded_media):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"📁 {file_info['name']}")
                st.write(f"Size: {file_info['size']} bytes")
            
            with col2:
                if file_info['type'].startswith('image'):
                    try:
                        img = Image.open(file_info['path'])
                        st.image(img, width=100)
                    except:
                        st.write("🖼️ Image")
                else:
                    st.write("🎥 Video")
            
            with col3:
                if st.button(f"Remove", key=f"remove_{i}"):
                    st.session_state.uploaded_media.pop(i)
                    st.rerun()

def create_sample_image(image_type):
    """Create sample images for demonstration"""
    img = np.ones((400, 600, 3), dtype=np.uint8) * 128
    
    if image_type == "bridge_crack":
        cv2.rectangle(img, (50, 50), (550, 350), (100, 100, 100), -1)
        cv2.line(img, (100, 100), (500, 300), (50, 50, 50), 3)
        cv2.putText(img, "Bridge Structure", (200, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
    elif image_type == "power_line":
        cv2.line(img, (0, 200), (600, 200), (80, 80, 80), 5)
        cv2.circle(img, (300, 200), 20, (200, 100, 50), -1)
        cv2.putText(img, "Power Line Infrastructure", (150, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
    elif image_type == "building":
        cv2.rectangle(img, (100, 100), (500, 350), (120, 120, 120), -1)
        cv2.rectangle(img, (150, 150), (200, 200), (80, 80, 80), -1)
        cv2.putText(img, "Building Facade", (200, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
    elif image_type == "road":
        cv2.rectangle(img, (0, 150), (600, 350), (60, 60, 60), -1)
        cv2.line(img, (0, 250), (600, 250), (255, 255, 255), 2)
        cv2.putText(img, "Road Surface", (200, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

def show_analysis_page():
    st.markdown('<h2 class="section-header">🤖 AI Analysis</h2>', unsafe_allow_html=True)
    
    # Check if media is uploaded
    if 'uploaded_media' not in st.session_state or not st.session_state.uploaded_media:
        st.warning("⚠️ Please upload media files first in the Media Upload section.")
        return
    
    # Model selection
    show_model_selection()
    
    # Analysis controls
    show_analysis_controls()
    
    # Run analysis
    if st.button("🚀 Run Inspection Analysis", type="primary"):
        run_inspection_analysis()

def show_model_selection():
    st.subheader("🧠 AI Model Selection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Available Models")
        
        models = {
            "Crack Detection": {"accuracy": "94.2%", "description": "Detects structural cracks"},
            "Corrosion Detection": {"accuracy": "91.8%", "description": "Identifies rust and corrosion"},
            "Thermal Anomaly": {"accuracy": "96.5%", "description": "Detects overheating"},
            "Vegetation Risk": {"accuracy": "89.3%", "description": "Identifies vegetation growth"},
            "Structural Damage": {"accuracy": "92.7%", "description": "General structural assessment"}
        }
        
        default_models = st.session_state.get('default_models', ["Crack Detection", "Corrosion Detection"])
        selected_models = st.multiselect(
            "Select detection models to use:",
            list(models.keys()),
            default=default_models
        )
        
        st.session_state.selected_models = selected_models
    
    with col2:
        st.markdown("### Model Details")
        
        if selected_models:
            for model_name in selected_models:
                model_info = models[model_name]
                
                with st.expander(f"📊 {model_name}"):
                    st.write(f"**Accuracy:** {model_info['accuracy']}")
                    st.write(f"**Description:** {model_info['description']}")

def show_analysis_controls():
    st.subheader("⚙️ Analysis Settings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        default_conf = st.session_state.get('default_confidence', 0.7)
        confidence_threshold = st.slider(
            "Confidence Threshold",
            min_value=0.1,
            max_value=1.0,
            value=float(default_conf),
            step=0.05
        )
        st.session_state.confidence_threshold = confidence_threshold
    
    with col2:
        detection_sensitivity = st.selectbox(
            "Detection Sensitivity",
            ["Low", "Medium", "High"],
            index=1
        )
        st.session_state.detection_sensitivity = detection_sensitivity
    
    with col3:
        analysis_mode = st.selectbox(
            "Analysis Mode",
            ["Quick Scan", "Detailed Analysis", "Comprehensive Report"],
            index=1
        )
        st.session_state.analysis_mode = analysis_mode

def run_inspection_analysis():
    """Run the AI inspection analysis on uploaded media"""
    
    if 'selected_models' not in st.session_state or not st.session_state.selected_models:
        st.error("Please select at least one AI model for analysis.")
        return
    
    st.subheader("🔍 Analysis in Progress...")
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Initialize results storage
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = []
    
    total_files = len(st.session_state.uploaded_media)
    
    for i, file_info in enumerate(st.session_state.uploaded_media):
        status_text.text(f"Analyzing {file_info['name']}...")
        progress_bar.progress((i + 1) / total_files)
        
        # Simulate analysis
        file_results = analyze_single_file(file_info)
        st.session_state.analysis_results.append(file_results)
    
    status_text.text("Analysis completed!")
    st.success("✅ Inspection analysis completed successfully!")
    
    # Display results summary
    display_analysis_summary()

def analyze_single_file(file_info):
    """Analyze a single file with selected models"""
    
    results = {
        'file_name': file_info['name'],
        'file_path': file_info['path'],
        'analysis_time': datetime.now(),
        'detections': []
    }
    
    # Simulate detections for each selected model
    for model_name in st.session_state.selected_models:
        num_detections = random.randint(0, 2)
        
        for _ in range(num_detections):
            confidence = random.uniform(st.session_state.confidence_threshold, 1.0)
            
            detection = {
                'model': model_name,
                'defect_type': f"{model_name} Defect",
                'confidence': confidence,
                'bbox': [100, 100, 200, 200],
                'severity': 'High' if confidence > 0.8 else 'Medium',
                'description': f"Defect detected by {model_name}"
            }
            
            results['detections'].append(detection)
    
    return results

def display_analysis_summary():
    """Display summary of analysis results"""
    
    if not st.session_state.analysis_results:
        return
    
    st.subheader("📈 Analysis Summary")
    
    # Calculate summary statistics
    total_detections = sum(len(result['detections']) for result in st.session_state.analysis_results)
    files_with_defects = sum(1 for result in st.session_state.analysis_results if result['detections'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Files Analyzed", len(st.session_state.analysis_results))
    
    with col2:
        st.metric("Files with Defects", files_with_defects)
    
    with col3:
        st.metric("Total Detections", total_detections)
    
    with col4:
        avg_confidence = 0
        if total_detections > 0:
            all_confidences = []
            for result in st.session_state.analysis_results:
                for detection in result['detections']:
                    all_confidences.append(detection['confidence'])
            avg_confidence = sum(all_confidences) / len(all_confidences)
        
        st.metric("Avg Confidence", f"{avg_confidence:.2f}")

def show_results_page():
    st.markdown('<h2 class="section-header">📊 Results & Reports</h2>', unsafe_allow_html=True)
    
    if 'analysis_results' not in st.session_state or not st.session_state.analysis_results:
        st.warning("⚠️ No analysis results available. Please run analysis first.")
        return
    
    # Results visualization
    show_detailed_results()
    
    # Export options
    show_export_options()

def show_detailed_results():
    st.subheader("🔍 Detailed Detection Results")
    
    for result in st.session_state.analysis_results:
        with st.expander(f"📁 {result['file_name']} - {len(result['detections'])} detections"):
            
            if result['detections']:
                # Display image with detections
                try:
                    img = Image.open(result['file_path'])
                    st.image(img, caption=result['file_name'], width=400)
                except:
                    st.write("Could not display image")
                
                # Detection details
                for i, detection in enumerate(result['detections']):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Detection {i+1}:**")
                        st.write(f"Type: {detection['defect_type']}")
                    
                    with col2:
                        st.write(f"**Confidence:** {detection['confidence']:.2f}")
                        st.write(f"**Severity:** {detection['severity']}")
                    
                    with col3:
                        st.write(f"**Model:** {detection['model']}")
                        st.write(f"**Description:** {detection['description']}")
            else:
                st.write("No defects detected in this file.")

def show_export_options():
    st.subheader("📤 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Generate PDF Report"):
            if 'analysis_results' in st.session_state and st.session_state.analysis_results:
                pdf_bytes = build_pdf_report()
                st.download_button(
                    label="Download Report.pdf",
                    data=pdf_bytes,
                    file_name=f"flyscope_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf"
                )
            else:
                st.info("No analysis results to include in the report.")
    
    with col2:
        if st.button("📊 Export CSV Data"):
            # Create CSV data
            csv_data = []
            for result in st.session_state.analysis_results:
                for detection in result['detections']:
                    csv_data.append({
                        'File': result['file_name'],
                        'Defect Type': detection['defect_type'],
                        'Confidence': detection['confidence'],
                        'Severity': detection['severity'],
                        'Model': detection['model']
                    })
            
            if csv_data:
                df = pd.DataFrame(csv_data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="inspection_results.csv",
                    mime="text/csv"
                )
    
    with col3:
        if st.button("🖼️ Export Annotated Images (ZIP)"):
            if 'annotations' in st.session_state and st.session_state.annotations:
                buffer = io.BytesIO()
                with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for name, path in st.session_state.annotations.items():
                        if os.path.exists(path):
                            zf.write(path, arcname=f"annotated_{name}.png")
                buffer.seek(0)
                st.download_button(
                    label="Download ZIP",
                    data=buffer,
                    file_name="annotated_images.zip",
                    mime="application/zip"
                )
            else:
                st.info("No annotations available yet. Use the Annotation Tool page.")

def build_pdf_report():
    """Build a PDF report from current session results and return bytes."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("FLYSCOPE Inspection Report", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Summary metrics
    results = st.session_state.get('analysis_results', [])
    total_files = len(results)
    total_detections = sum(len(r['detections']) for r in results)
    files_with_defects = sum(1 for r in results if r['detections'])

    data = [["Metric", "Value"], ["Total Files Analyzed", str(total_files)], ["Files with Defects", str(files_with_defects)], ["Total Detections", str(total_detections)]]
    table = Table(data, colWidths=[200, 300])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f3f4f6')),
    ]))
    story.append(table)
    story.append(Spacer(1, 18))

    # Per-file sections
    for res in results:
        story.append(Paragraph(f"File: {res['file_name']}", styles['Heading3']))
        story.append(Spacer(1, 6))
        # Thumbnail if image
        try:
            if os.path.exists(res['file_path']):
                # Safely try to include a small thumbnail for images
                pil = Image.open(res['file_path'])
                thumb_path = None
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                    pil.thumbnail((512, 512))
                    pil.save(tmp.name)
                    thumb_path = tmp.name
                story.append(RLImage(thumb_path, width=200, height=200*pil.height/pil.width))
                story.append(Spacer(1, 6))
        except Exception:
            pass

        if res['detections']:
            det_data = [["Type", "Severity", "Confidence", "Model", "Description"]]
            for d in res['detections']:
                det_data.append([d.get('defect_type','-'), d.get('severity','-'), f"{d.get('confidence',0):.2f}", d.get('model','-'), d.get('description','-')])
            det_table = Table(det_data, colWidths=[120, 70, 70, 100, 240])
            det_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#111827')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
                ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8fafc')),
            ]))
            story.append(det_table)
        else:
            story.append(Paragraph("No defects detected.", styles['Italic']))
        story.append(Spacer(1, 18))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def show_mapping_page():
    st.markdown('<h2 class="section-header">🗺️ Fault Mapping</h2>', unsafe_allow_html=True)
    
    if 'analysis_results' not in st.session_state or not st.session_state.analysis_results:
        st.warning("⚠️ No analysis results available for mapping.")
        return
    
    # Create map
    m = folium.Map(location=[11.1271, 78.6569], zoom_start=7, tiles='cartodbpositron')
    
    # Build fault points from results (randomized geotags for demo)
    fault_locations = []
    for result in st.session_state.analysis_results:
        for det in result['detections']:
            # Random demo coordinates around TN center if not provided
            lat = 10.5 + random.uniform(-1.5, 1.5)
            lon = 78.0 + random.uniform(-1.5, 1.5)
            fault_locations.append({
                "lat": lat,
                "lon": lon,
                "fault": det['defect_type'],
                "severity": det['severity'],
                "confidence": det['confidence']
            })

    # Clusters
    cluster = MarkerCluster().add_to(m)
    for loc in fault_locations:
        color = "red" if loc["severity"] in ["High", "Critical"] else ("orange" if loc["severity"] == "Medium" else "green")
        folium.CircleMarker(
            [loc["lat"], loc["lon"]],
            radius=6,
            color=color,
            fill=True,
            fill_opacity=0.8,
            popup=f"⚠️ {loc['fault']} | Severity: {loc['severity']} | Conf: {loc['confidence']:.2f}"
        ).add_to(cluster)

    # Heatmap by confidence
    if fault_locations:
        heat_data = [[loc['lat'], loc['lon'], float(loc['confidence'])] for loc in fault_locations]
        HeatMap(heat_data, radius=18, blur=25, min_opacity=0.3).add_to(m)
    
    # Display map
    st_folium(m, width=700, height=500)
    
    # Fault statistics
    st.subheader("📊 Fault Distribution")
    
    severity_data = {"Critical": 2, "High": 1, "Medium": 1, "Low": 0}
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Severity pie chart
        fig = px.pie(
            values=list(severity_data.values()),
            names=list(severity_data.keys()),
            title="Fault Severity Distribution"
        )
        st.plotly_chart(fig)
    
    with col2:
        # Fault type breakdown
        fault_types = {"Thermal": 1, "Vegetation": 1, "Corrosion": 1, "Structural": 1}
        
        fig = px.bar(
            x=list(fault_types.keys()),
            y=list(fault_types.values()),
            title="Fault Type Distribution"
        )
        st.plotly_chart(fig)

def show_data_management_page():
    st.markdown('<h2 class="section-header">📁 Data Management</h2>', unsafe_allow_html=True)
    
    # Dataset viewer
    st.subheader("📊 Inspection History")
    
    if 'analysis_results' in st.session_state and st.session_state.analysis_results:
        # Create summary table
        summary_data = []
        for result in st.session_state.analysis_results:
            summary_data.append({
                'File Name': result['file_name'],
                'Analysis Time': result['analysis_time'].strftime('%Y-%m-%d %H:%M:%S'),
                'Detections': len(result['detections']),
                'Status': 'Completed'
            })
        
        df = pd.DataFrame(summary_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No inspection data available yet.")
    
    # Data management options
    st.subheader("🔧 Data Management Tools")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Clear All Data"):
            if 'uploaded_media' in st.session_state:
                del st.session_state.uploaded_media
            if 'analysis_results' in st.session_state:
                del st.session_state.analysis_results
            st.success("All data cleared!")
            st.rerun()
    
    with col2:
        if st.button("📥 Import Dataset"):
            st.info("Dataset import feature coming soon!")
    
    with col3:
        if st.button("💾 Backup Data"):
            st.info("Data backup feature coming soon!")

def show_settings_page():
    st.markdown('<h2 class="section-header">⚙️ Settings</h2>', unsafe_allow_html=True)
    theme = st.selectbox("Theme", ["Dark", "Light"], index=0 if st.session_state.get('theme','Dark')=='Dark' else 1)
    default_conf = st.slider("Default Confidence Threshold", 0.1, 1.0, float(st.session_state.get('default_confidence', 0.7)), 0.05)
    available_models = ["Crack Detection", "Corrosion Detection", "Thermal Anomaly", "Vegetation Risk", "Structural Damage"]
    default_models = st.multiselect("Default Selected Models", available_models, default=st.session_state.get('default_models', ["Crack Detection", "Corrosion Detection"]))

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save Settings"):
            st.session_state.theme = theme
            st.session_state.default_confidence = float(default_conf)
            st.session_state.default_models = default_models
            st.success("Settings saved")
            st.rerun()
    with col2:
        if st.button("Reset to Defaults"):
            st.session_state.theme = 'Dark'
            st.session_state.default_confidence = 0.7
            st.session_state.default_models = ["Crack Detection", "Corrosion Detection"]
            st.success("Reset completed")
            st.rerun()

if __name__ == "__main__":
    main()
