import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("Drone Inspection Digital Twin Dashboard")

# Sample drone inspection points
locations = [
    {"lat": 12.9716, "lon": 77.5946, "fault": "Crack Detected", "severity": "High"},
    {"lat": 12.9720, "lon": 77.5950, "fault": "Rust Detected", "severity": "Medium"}
]

# Map
m = folium.Map(location=[12.9716, 77.5946], zoom_start=15)
for loc in locations:
    folium.Marker(
        [loc["lat"], loc["lon"]],
        popup=f"{loc['fault']} | Severity: {loc['severity']}",
        icon=folium.Icon(color="red")
    ).add_to(m)

st_map = st_folium(m, width=700, height=500)

# Predictive Maintenance Result
st.subheader("Predictive Maintenance Alert")
st.write("⚠️ Insulator Failure Probability: **72%**")

