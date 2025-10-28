import streamlit as st
import folium
from streamlit_folium import st_folium
from ui import render_top_nav
from sidebar_nav import render_sidebar_navigation

# Import page components that are now in the 'components' directory
from components.upload_page import show_upload_page
from components.analysis_page import show_analysis_page
from components.annotation_page import show_annotation_page
from components.admin_panel import show_admin_panel
from components._login import show_login_page

# Page config and modern design system
st.set_page_config(
    page_title="INFRA-SCOPE – Smart Damage Detection for Safer Infrastructure | Tamil Nadu Grid", 
    page_icon="🏗️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with modern design system
st.markdown(
    """
    <style>
    /* Global Design System */
    :root {
        --primary-color: #0ea5e9;
        --primary-dark: #0284c7;
        --secondary-color: #64748b;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --background-dark: #0f172a;
        --card-background: #1e293b;
        --border-color: #334155;
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --text-muted: #64748b;
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --border-radius: 12px;
        --border-radius-sm: 8px;
    }
    
    /* Typography */
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(135deg, var(--primary-color), #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.1;
    }
    
    .hero-subtitle {
        color: var(--text-secondary);
        font-size: 1.25rem;
        margin-bottom: 2rem;
        font-weight: 400;
        line-height: 1.6;
    }
    
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        color: var(--text-primary);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Components */
    .pill {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 999px;
        background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
        color: white;
        font-size: 0.875rem;
        font-weight: 600;
        box-shadow: var(--shadow);
        margin-bottom: 1.5rem;
    }
    
    .modern-card {
        background: var(--card-background);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        box-shadow: var(--shadow);
        margin-bottom: 1.5rem;
        transition: all 0.2s ease;
    }
    
    .modern-card:hover {
        box-shadow: var(--shadow-lg);
        border-color: var(--primary-color);
    }
    
    .metric-card {
        background: var(--card-background);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        text-align: center;
        box-shadow: var(--shadow);
        transition: all 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.875rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Status indicators */
    .status-critical { color: var(--error-color); }
    .status-high { color: var(--warning-color); }
    .status-medium { color: var(--success-color); }
    .status-low { color: var(--text-muted); }
    
    /* Improved spacing */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem;
        border-radius: var(--border-radius-sm);
        background: var(--card-background);
        border: 1px solid var(--border-color);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-color) !important;
        color: white !important;
        border-color: var(--primary-color) !important;
    }
    
    /* Sidebar improvements */
    .css-1d391kg {
        background: var(--background-dark);
    }
    
    .stSelectbox > div > div {
        background: var(--card-background);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-sm);
    }
    
    /* Button improvements */
    .stButton > button {
        border-radius: var(--border-radius-sm);
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state for page navigation if it doesn't exist
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Render the custom sidebar and top navigation
render_sidebar_navigation()
render_top_nav()

# Hero Section with improved layout
st.markdown(
    """
    <div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem;">
        <div class="pill">Tamil Nadu Grid</div>
        <h1 class="hero-title">🏗️ INFRA-SCOPE – Smart Damage Detection for Safer Infrastructure</h1>
        <p class="hero-subtitle">AI-powered damage detection for safer, smarter infrastructure monitoring</p>
    </div>
    """,
    unsafe_allow_html=True
)

def show_home_page():
    # Domain dataset (district sample incidents)
    district_data = {
        "Chennai": [
            {"lat": 13.0827, "lon": 80.2707, "fault": "Overheating Connector (Thermal)", "severity": "Critical"},
            {"lat": 12.9165, "lon": 80.2295, "fault": "Rust on Insulator Clamp", "severity": "Medium"},
        ],
        "Kanchipuram": [
            {"lat": 12.6940, "lon": 79.9776, "fault": "Vegetation Risk near Power Line", "severity": "High"},
            {"lat": 12.85, "lon": 79.7, "fault": "Corrosion on Tower Base", "severity": "Medium"},
        ],
        "Madurai": [
            {"lat": 9.9252, "lon": 78.1198, "fault": "Damaged Cross-arm", "severity": "High"},
            {"lat": 9.95, "lon": 78.15, "fault": "Bird Nest Obstruction", "severity": "Low"},
        ],
        "Coimbatore": [
            {"lat": 11.0168, "lon": 76.9558, "fault": "Thermal Hotspot on Connector", "severity": "High"},
            {"lat": 11.05, "lon": 76.9, "fault": "Vegetation Growth close to Line", "severity": "Critical"},
        ],
        "Trichy": [
            {"lat": 10.7905, "lon": 78.7047, "fault": "Rust on Bolts and Joints", "severity": "Medium"},
            {"lat": 10.82, "lon": 78.68, "fault": "Tower Tilt Detected", "severity": "High"},
        ],
        "Salem": [
            {"lat": 11.6643, "lon": 78.1460, "fault": "Insulator Flashover Risk", "severity": "Critical"},
            {"lat": 11.7, "lon": 78.15, "fault": "Partial Conductor Damage", "severity": "High"},
        ],
    }

    # Dashboard Controls (moved to main content area)
    st.markdown("### 🎛️ Dashboard Controls")
    filter_col1, filter_col2 = st.columns([1, 1])

    with filter_col1:
        st.markdown("**📍 Select District**")
        district = st.selectbox(
            "District", 
            list(district_data.keys()), 
            index=0,
            help="Choose a district to view specific infrastructure data"
        )

    with filter_col2:
        st.markdown("**⚠️ Severity Levels**")
        severity_filter = st.multiselect(
            "Filter by severity", 
            ["Critical", "High", "Medium", "Low"], 
            default=["Critical", "High", "Medium", "Low"],
            help="Select which severity levels to display on the dashboard"
        )

    st.info("💡 Use the filters above to customize your view and focus on specific areas or severity levels.")
    st.markdown("---")

    # Compute KPIs
    all_incidents = [i for inc in district_data.values() for i in inc]
    district_incidents = [i for i in district_data[district] if i["severity"] in severity_filter]
    total_sites = len(all_incidents)
    district_sites = len(district_incidents)
    critical_ct = sum(1 for i in all_incidents if i["severity"] == "Critical")

    # Enhanced KPI Section with modern cards
    st.markdown("### 📊 Key Performance Indicators")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{total_sites}</div>
                <div class="metric-label">Total Sites</div>
                <div style="color: var(--text-muted); font-size: 0.75rem; margin-top: 0.5rem;">Statewide</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{district_sites}</div>
                <div class="metric-label">District Sites</div>
                <div style="color: var(--text-muted); font-size: 0.75rem; margin-top: 0.5rem;">{district}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value status-critical">{critical_ct}</div>
                <div class="metric-label">Critical Issues</div>
                <div style="color: var(--error-color); font-size: 0.75rem; margin-top: 0.5rem;">Needs Attention</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        completion_rate = round((total_sites - critical_ct) / total_sites * 100) if total_sites > 0 else 0
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value status-medium">{completion_rate}%</div>
                <div class="metric-label">Health Score</div>
                <div style="color: var(--success-color); font-size: 0.75rem; margin-top: 0.5rem;">Overall Status</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Enhanced Tabs Section
    st.markdown("<br>", unsafe_allow_html=True)
    tab_overview, tab_map, tab_alerts, tab_howto = st.tabs([
        "📋 Overview",
        "🗺️ Interactive Map", 
        "🔮 Predictive Alerts",
        "❓ How to Use"
    ])

    with tab_overview:
        st.markdown(f"### 📍 {district} District Overview")
        
        col_info, col_chart = st.columns([2, 1])
        
        with col_info:
            st.markdown(
                """
                <div class="modern-card">
                    <h4>🎯 Dashboard Purpose</h4>
                    <p>This dashboard highlights infrastructure anomalies detected across the Tamil Nadu grid using advanced AI-powered drone inspection technology.</p>
                    <p>Use the sidebar filters to focus on specific districts and severity levels for detailed analysis.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col_chart:
            if district_incidents:
                severity_counts = {}
                for incident in district_incidents:
                    severity = incident["severity"]
                    severity_counts[severity] = severity_counts.get(severity, 0) + 1
                
                st.markdown("**Severity Distribution**")
                for severity, count in severity_counts.items():
                    color_class = f"status-{severity.lower()}"
                    st.markdown(f"<span class='{color_class}'>● {severity}: {count}</span>", unsafe_allow_html=True)

        # Enhanced incident table
        if district_incidents:
            st.markdown("### 📊 Recent Incidents")
            
            # Create enhanced dataframe with better formatting
            incidents_df = []
            for i, incident in enumerate(district_incidents):
                severity_color = {
                    "Critical": "🔴",
                    "High": "🟠", 
                    "Medium": "🟡",
                    "Low": "🟢"
                }.get(incident["severity"], "⚪")
                
                incidents_df.append({
                    "#": i + 1,
                    "Status": f"{severity_color} {incident['severity']}",
                    "Fault Type": incident["fault"],
                    "Latitude": f"{incident['lat']:.4f}",
                    "Longitude": f"{incident['lon']:.4f}",
                    "Priority": "High" if incident["severity"] in ["Critical", "High"] else "Normal"
                })
            
            st.dataframe(
                incidents_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.markdown(
                """
                <div class="modern-card" style="text-align: center; padding: 3rem;">
                    <h4>🎉 No Issues Found</h4>
                    <p>Great news! No incidents match your current filter criteria.</p>
                    <p>Try adjusting the severity filters to see more data.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    with tab_map:
        st.subheader("Interactive Map")
        m = folium.Map(location=[11.1271, 78.6569], zoom_start=7)
        for loc in district_incidents:
            color = "red" if loc["severity"] in ["High", "Critical"] else "orange"
            folium.Marker(
                [loc["lat"], loc["lon"]],
                popup=f"⚠️ {loc['fault']} | Severity: {loc['severity']}",
                icon=folium.Icon(color=color, icon="info-sign"),
            ).add_to(m)
        st_folium(m, width=900, height=520)

    with tab_alerts:
        st.subheader("🔮 Predictive Maintenance Alerts")
        guidance = {
            "Chennai": [
                "⚡ Tower #42 (Tambaram): Failure Probability 78%",
                "⚡ Insulator at Sriperumbudur Line: Failure Probability 65%",
                "⚡ Vegetation near Chengalpattu Line: Immediate Clearance Needed",
            ],
            "Madurai": [
                "⚡ Tower #18 (Thiruparankundram): Failure Probability 72%",
                "⚡ Insulator at Melur Line: Failure Probability 54%",
                "⚡ Vegetation near Usilampatti Line: Moderate Risk",
            ],
            "Coimbatore": [
                "⚡ Tower #27 (Pollachi): Failure Probability 80%",
                "⚡ Connector at Mettupalayam Line: Failure Probability 69%",
                "⚡ Vegetation near Sulur Line: Immediate Clearance Needed",
            ],
            "Trichy": [
                "⚡ Tower #11 (Srirangam): Failure Probability 70%",
                "⚡ Insulator at Lalgudi Line: Failure Probability 58%",
                "⚡ Vegetation near Manapparai Line: Moderate Risk",
            ],
            "Salem": [
                "⚡ Tower #35 (Omalur): Failure Probability 76%",
                "⚡ Insulator at Edappadi Line: Failure Probability 64%",
                "⚡ Conductor near Attur Line: High Risk – Immediate Action Needed",
            ],
            "Kanchipuram": [
                "⚡ Tower #22 (Kanchipuram): Failure Probability 74%",
                "⚡ Insulator at Walajabad Line: Failure Probability 60%",
                "⚡ Vegetation near Uthiramerur Line: Clearance Needed Soon",
            ],
        }
        for line in guidance.get(district, []):
            st.write(f"- {line}")

    with tab_howto:
        st.subheader("How to Use this Application")
        st.markdown(
            """
            1. Upload drone imagery or video in the INFRA-SCOPE main app (sidebar → Navigation → "📤 Media Upload").
            2. Choose AI models (crack/corrosion/thermal/vegetation) and run analysis ("🤖 AI Analysis").
            3. Review detections and export a PDF/CSV report ("📊 Results & Reports").
            4. Visualize fault distribution on the map and plan maintenance ("🗺️ Fault Mapping").
            5. Iterate with new missions to continuously improve coverage and safety.

            Tips
            - Use the severity filter on the left to focus on critical hotspots.
            - Hover markers on the Map tab to view fault details at a location.
            - Start with sample images in the main app to explore the full workflow quickly.
            """
        )

# Main router logic to display the correct page
if st.session_state.page == 'home':
    show_home_page()
elif st.session_state.page == 'upload':
    show_upload_page()
elif st.session_state.page == 'analysis':
    show_analysis_page()
elif st.session_state.page == 'annotation':
    show_annotation_page()
elif st.session_state.page == 'admin':
    show_admin_panel()
elif st.session_state.page == 'login':
    show_login_page()
