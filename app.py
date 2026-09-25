import streamlit as st
import pandas as pd
import json

# Page configuration
st.set_page_config(
    page_title="Global SEZ Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Global Special Economic Zones (SEZ) Dashboard")
st.write("Explore global special economic zones, free zones, and industrial estates using your uploaded datasets.")

# Sidebar navigation for datasets
st.sidebar.header("Navigation")
data_source = st.sidebar.radio(
    "Select Dataset",
    ["GeoJSON Spatial Data", "CSV Zones Data"]
)

# Cached function to load GeoJSON safely using standard json
@st.cache_data
def load_geojson():
    with open("ciip_sez_ntl_2017.geojson", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Extract features if it's a FeatureCollection
    if "features" in data:
        features = data["features"]
        # Extract properties and discard complex geometries if they cause trouble
        records = []
        for feature in features:
            props = feature.get("properties", {})
            records.append(props)
        return pd.DataFrame(records)
    return pd.DataFrame()

# Cached function to load CSV
@st.cache_data
def load_csv():
    return pd.read_csv("zones.csv")

# Display GeoJSON Data
if data_source == "GeoJSON Spatial Data":
    st.subheader("Spatial Data View (`ciip_sez_ntl_2017.geojson`)")
    
    try:
        df = load_geojson()
        st.metric(label="Total Zones in GeoJSON", value=len(df))

        st.write("### Data Table Preview")
        st.dataframe(df)
        
    except Exception as e:
        st.error(f"Error loading GeoJSON file: {e}")

# Display CSV Data
else:
    st.subheader("Tabular Data View (`zones.csv`)")
    
    try:
        df = load_csv()
        st.metric(label="Total Records in CSV", value=len(df))
        
        st.write("### Data Table Preview")
        st.dataframe(df)
        
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
