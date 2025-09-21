import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("🚁 Drone-based Infrastructure Inspection - Tamil Nadu Grid")

# Inspection data for Tamil Nadu districts
district_data = {
    "Chennai": [
        {"lat": 13.0827, "lon": 80.2707, "fault": "Overheating Connector Detected (Thermal)", "severity": "Critical"},
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
    ]
}

# Dropdown for district selection
district = st.selectbox("Select a District", list(district_data.keys()))

# Map centered on Tamil Nadu
m = folium.Map(location=[11.1271, 78.6569], zoom_start=7)

# Plot markers only for the selected district
for loc in district_data[district]:
    color = "red" if loc["severity"] in ["High", "Critical"] else "orange"
    folium.Marker(
        [loc["lat"], loc["lon"]],
        popup=f"⚠️ {loc['fault']} | Severity: {loc['severity']}",
        icon=folium.Icon(color=color, icon="info-sign")
    ).add_to(m)

# Show map
st_map = st_folium(m, width=700, height=500)

# Predictive Maintenance Alerts
st.subheader("🔮 Predictive Maintenance Alerts")
if district == "Chennai":
    st.write("""
    - ⚡ Transmission Tower #42 (Tambaram): Failure Probability **78%**  
    - ⚡ Insulator at Sriperumbudur Line: Failure Probability **65%**  
    - ⚡ Vegetation near Chengalpattu Line: Immediate Clearance Needed  
    """)
elif district == "Madurai":
    st.write("""
    - ⚡ Tower #18 (Thiruparankundram): Failure Probability **72%**  
    - ⚡ Insulator at Melur Line: Failure Probability **54%**  
    - ⚡ Vegetation near Usilampatti Line: Moderate Risk  
    """)
elif district == "Coimbatore":
    st.write("""
    - ⚡ Tower #27 (Pollachi): Failure Probability **80%**  
    - ⚡ Connector at Mettupalayam Line: Failure Probability **69%**  
    - ⚡ Vegetation near Sulur Line: Immediate Clearance Needed  
    """)
elif district == "Trichy":
    st.write("""
    - ⚡ Tower #11 (Srirangam): Failure Probability **70%**  
    - ⚡ Insulator at Lalgudi Line: Failure Probability **58%**  
    - ⚡ Vegetation near Manapparai Line: Moderate Risk  
    """)
elif district == "Salem":
    st.write("""
    - ⚡ Tower #35 (Omalur): Failure Probability **76%**  
    - ⚡ Insulator at Edappadi Line: Failure Probability **64%**  
    - ⚡ Conductor near Attur Line: High Risk – Immediate Action Needed  
    """)
elif district == "Kanchipuram":
    st.write("""
    - ⚡ Tower #22 (Kanchipuram): Failure Probability **74%**  
    - ⚡ Insulator at Walajabad Line: Failure Probability **60%**  
    - ⚡ Vegetation near Uthiramerur Line: Clearance Needed Soon  
    """)
