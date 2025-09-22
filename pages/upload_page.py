import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile
import os

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

def handle_live_camera():
    st.subheader("Live Drone Camera Connection")
    st.info("🚧 Live camera integration coming soon!")
    
    # Drone connection options
    drone_type = st.selectbox(
        "Select Drone Type:",
        ["DJI Tello", "DJI Mini", "Custom Drone", "Simulator"]
    )
    
    if drone_type == "Simulator":
        st.warning("Using camera simulator mode")
        if st.button("Start Camera Simulation"):
            simulate_camera_feed()

def handle_sample_images():
    st.subheader("Sample Infrastructure Images")
    
    # Create sample images for demonstration
    sample_images = {
        "Bridge Crack": create_sample_image("bridge_crack"),
        "Power Line Corrosion": create_sample_image("power_line"),
        "Building Damage": create_sample_image("building"),
        "Road Surface": create_sample_image("road")
    }
    
    selected_samples = st.multiselect(
        "Select sample images to analyze:",
        list(sample_images.keys())
    )
    
    if selected_samples:
        if 'uploaded_media' not in st.session_state:
            st.session_state.uploaded_media = []
        
        for sample_name in selected_samples:
            # Save sample image
            img = sample_images[sample_name]
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

def display_uploaded_files():
    if 'uploaded_media' in st.session_state and st.session_state.uploaded_media:
        st.subheader("Uploaded Files")
        
        for i, file_info in enumerate(st.session_state.uploaded_media):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"📁 {file_info['name']}")
                st.write(f"Size: {file_info['size']} bytes")
                # Image quality metrics
                if file_info['type'].startswith('image'):
                    try:
                        img_cv = cv2.imread(file_info['path'])
                        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
                        # Blur estimate via Laplacian variance
                        fm = cv2.Laplacian(gray, cv2.CV_64F).var()
                        # Brightness estimate
                        brightness = float(np.mean(gray))
                        blur_quality = "Good" if fm > 100.0 else ("OK" if fm > 50.0 else "Blurry")
                        st.caption(f"Blur score: {fm:.1f} ({blur_quality}) | Brightness: {brightness:.0f}/255")
                    except Exception:
                        pass
            
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

def simulate_camera_feed():
    st.subheader("Camera Simulation")
    
    # Create a simple camera simulation
    camera_placeholder = st.empty()
    
    # Simulate camera frames
    for i in range(5):
        # Create a simple simulated frame
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        frame = cv2.putText(frame, f"Drone Camera - Frame {i+1}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        camera_placeholder.image(frame, channels="BGR", caption=f"Live Feed - Frame {i+1}")
        
        if i == 4:  # Last frame
            if st.button("Capture Frame"):
                # Save captured frame
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                    cv2.imwrite(tmp_file.name, frame)
                    
                    file_info = {
                        'name': f"captured_frame.jpg",
                        'path': tmp_file.name,
                        'type': 'image/jpeg',
                        'size': os.path.getsize(tmp_file.name)
                    }
                    
                    if 'uploaded_media' not in st.session_state:
                        st.session_state.uploaded_media = []
                    
                    st.session_state.uploaded_media.append(file_info)
                    st.success("Frame captured successfully!")

def create_sample_image(image_type):
    """Create sample images for demonstration"""
    img = np.ones((400, 600, 3), dtype=np.uint8) * 128
    
    if image_type == "bridge_crack":
        # Simulate a bridge with cracks
        cv2.rectangle(img, (50, 50), (550, 350), (100, 100, 100), -1)
        cv2.line(img, (100, 100), (500, 300), (50, 50, 50), 3)
        cv2.putText(img, "Bridge Structure", (200, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
    elif image_type == "power_line":
        # Simulate power lines
        cv2.line(img, (0, 200), (600, 200), (80, 80, 80), 5)
        cv2.circle(img, (300, 200), 20, (200, 100, 50), -1)
        cv2.putText(img, "Power Line Infrastructure", (150, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
    elif image_type == "building":
        # Simulate building facade
        cv2.rectangle(img, (100, 100), (500, 350), (120, 120, 120), -1)
        cv2.rectangle(img, (150, 150), (200, 200), (80, 80, 80), -1)
        cv2.putText(img, "Building Facade", (200, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
    elif image_type == "road":
        # Simulate road surface
        cv2.rectangle(img, (0, 150), (600, 350), (60, 60, 60), -1)
        cv2.line(img, (0, 250), (600, 250), (255, 255, 255), 2)
        cv2.putText(img, "Road Surface", (200, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# Ensure the page renders when used in Streamlit's multipage mode
show_upload_page()
