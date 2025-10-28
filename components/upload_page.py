import streamlit as st
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    st.warning("OpenCV not installed. Some image analysis features may be limited.")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

from PIL import Image
import tempfile
import os
from auth import require_login, current_user
from ui import render_top_nav

def show_upload_page():
    st.markdown('<h2 class="section-header">📤 Media Upload</h2>', unsafe_allow_html=True)
    # Require authentication to access this page
    require_login()
    user = current_user()
    if user:
        st.caption(f"Logged in as @{user['username']} ({user['email']})")
    st.divider()
    
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
            # Check if file already exists to prevent duplicates
            file_exists = any(
                existing_file['name'] == uploaded_file.name and 
                existing_file['size'] == uploaded_file.size
                for existing_file in st.session_state.uploaded_media
            )
            
            if not file_exists:
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
                
                # Check if sample image already exists to prevent duplicates
                sample_exists = any(
                    existing_file['name'] == file_info['name']
                    for existing_file in st.session_state.uploaded_media
                )
                
                if not sample_exists:
                    st.session_state.uploaded_media.append(file_info)
        
        st.success(f"Added {len(selected_samples)} sample image(s)")
        display_uploaded_files()

def display_uploaded_files():
    if 'uploaded_media' in st.session_state and st.session_state.uploaded_media:
        st.subheader("Uploaded Files")
        
        # Create a copy of the list to avoid modification during iteration
        files_to_display = st.session_state.uploaded_media.copy()
        
        for i, file_info in enumerate(files_to_display):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"📁 {file_info['name']}")
                st.write(f"Size: {file_info['size']} bytes")
                # Image quality metrics
                if file_info['type'].startswith('image') and CV2_AVAILABLE and NUMPY_AVAILABLE:
                    try:
                        img_cv = cv2.imread(file_info['path'])
                        if img_cv is not None:
                            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
                            # Blur estimate via Laplacian variance
                            fm = cv2.Laplacian(gray, cv2.CV_64F).var()
                            # Brightness estimate
                            brightness = float(np.mean(gray))
                            blur_quality = "Good" if fm > 100.0 else ("OK" if fm > 50.0 else "Blurry")
                            st.caption(f"Blur score: {fm:.1f} ({blur_quality}) | Brightness: {brightness:.0f}/255")
                    except Exception:
                        pass
                elif file_info['type'].startswith('image'):
                    st.caption("Install OpenCV for image quality analysis")
            
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
                # Use unique key based on file path instead of index
                unique_key = f"remove_{file_info['path'].replace('/', '_').replace('\\', '_')}"
                if st.button(f"Remove", key=unique_key):
                    # Remove the specific file from the list
                    try:
                        # Clean up the temporary file
                        if os.path.exists(file_info['path']):
                            os.unlink(file_info['path'])
                    except Exception:
                        pass  # File might already be deleted
                    
                    # Remove from session state using the actual file_info object
                    if file_info in st.session_state.uploaded_media:
                        st.session_state.uploaded_media.remove(file_info)
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
    # Import PIL Image at the top of function to avoid scope issues
    from PIL import Image as PILImage, ImageDraw
    
    if not CV2_AVAILABLE or not NUMPY_AVAILABLE:
        # Create a simple PIL image if cv2/numpy not available
        pil_img = PILImage.new('RGB', (600, 400), color=(128, 128, 128))
        draw = ImageDraw.Draw(pil_img)
        
        # Simple text-based sample
        title_map = {
            "bridge_crack": "Bridge Structure Sample",
            "power_line": "Power Line Sample", 
            "building": "Building Facade Sample",
            "road": "Road Surface Sample"
        }
        
        title = title_map.get(image_type, "Sample Image")
        draw.text((50, 50), title, fill=(255, 255, 255))
        draw.rectangle([100, 100, 500, 300], outline=(200, 200, 200), width=3)
        
        return pil_img
    
    # Original cv2-based implementation
    cv2_img = np.ones((400, 600, 3), dtype=np.uint8) * 128
    
    if image_type == "bridge_crack":
        # Simulate a bridge with cracks
        cv2.rectangle(cv2_img, (50, 50), (550, 350), (100, 100, 100), -1)
        cv2.line(cv2_img, (100, 100), (500, 300), (50, 50, 50), 3)
        cv2.putText(cv2_img, "Bridge Structure", (200, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
    elif image_type == "power_line":
        # Simulate power lines
        cv2.line(cv2_img, (0, 200), (600, 200), (80, 80, 80), 5)
        cv2.circle(cv2_img, (300, 200), 20, (200, 100, 50), -1)
        cv2.putText(cv2_img, "Power Line Infrastructure", (150, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
    elif image_type == "building":
        # Simulate building facade
        cv2.rectangle(cv2_img, (100, 100), (500, 350), (120, 120, 120), -1)
        cv2.rectangle(cv2_img, (150, 150), (200, 200), (80, 80, 80), -1)
        cv2.putText(cv2_img, "Building Facade", (200, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
    elif image_type == "road":
        # Simulate road surface
        cv2.rectangle(cv2_img, (0, 150), (600, 350), (60, 60, 60), -1)
        cv2.line(cv2_img, (0, 250), (600, 250), (255, 255, 255), 2)
        cv2.putText(cv2_img, "Road Surface", (200, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    return PILImage.fromarray(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))

# Note: This function should only be called from the main app router, not at module level
