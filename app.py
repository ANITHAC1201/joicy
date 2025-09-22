import streamlit as st
import folium
from streamlit_folium import st_folium

# Page config and custom style
st.set_page_config(page_title="FLYSCOPE | Tamil Nadu Grid", page_icon="🚁", layout="wide")
st.markdown(
    """
    <style>
      .hero-title {font-size: 2.4rem; font-weight: 800; margin: 0;}
      .hero-sub {color: #64748b; margin-bottom: 1.5rem;}
      .pill {display:inline-block; padding: .25rem .6rem; border-radius: 999px; background:#0ea5e9; color:white; font-size:.8rem;}
      .shadow-card {background:#0b1220; border:1px solid #1f2937; border-radius:10px; padding:1rem;}
      .table th, .table td {padding:.4rem .6rem}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="pill">Tamil Nadu Grid</div>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">🚁 Drone-based Infrastructure Inspection</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">Smart AI assistance for power-line towers, substations, and corridors.</p>', unsafe_allow_html=True)

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

# Sidebar controls
st.sidebar.header("Filters")
district = st.sidebar.selectbox("District", list(district_data.keys()), index=0)
severity_filter = st.sidebar.multiselect(
    "Severity", ["Critical", "High", "Medium", "Low"], default=["Critical", "High", "Medium", "Low"]
)

# Compute KPIs
all_incidents = [i for inc in district_data.values() for i in inc]
district_incidents = [i for i in district_data[district] if i["severity"] in severity_filter]
total_sites = len(all_incidents)
district_sites = len(district_incidents)
critical_ct = sum(1 for i in all_incidents if i["severity"] == "Critical")

k1, k2, k3 = st.columns(3)
with k1:
    st.metric("Total flagged sites (state)", total_sites)
with k2:
    st.metric(f"Flagged in {district}", district_sites)
with k3:
    st.metric("Critical hot-spots", critical_ct)

tab_overview, tab_map, tab_alerts, tab_howto = st.tabs([
    "Overview",
    "Map",
    "Predictive Alerts",
    "How to Use",
])

with tab_overview:
    st.subheader(f"Snapshot: {district}")
    st.write(
        "This dashboard highlights infrastructure anomalies detected across the Tamil Nadu grid. "
        "Use the filters to focus on a district and severity levels."
    )

    # Small incident table
    if district_incidents:
        st.markdown("#### Recent Incidents")
        st.dataframe(
            [{"Latitude": i["lat"], "Longitude": i["lon"], "Fault": i["fault"], "Severity": i["severity"]} for i in district_incidents],
            use_container_width=True,
        )
    else:
        st.info("No incidents for the selected filters.")

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
        1. Upload drone imagery or video in the FLYSCOPE main app (sidebar → Navigation → "📤 Media Upload").
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
