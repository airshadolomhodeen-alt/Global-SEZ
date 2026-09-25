import streamlit as st
import geopandas as gpd
import pandas as pd

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

# Cached function to load GeoJSON
@st.cache_data
def load_geojson():
    return gpd.read_file("ciip_sez_ntl_2017.geojson")

# Cached function to load CSV
@st.cache_data
def load_csv():
    return pd.read_csv("zones.csv")

# Display GeoJSON Data
if data_source == "GeoJSON Spatial Data":
    st.subheader("Spatial Data View (`ciip_sez_ntl_2017.geojson`)")
    
    try:
        gdf = load_geojson()
        st.metric(label="Total Zones in GeoJSON", value=len(gdf))
        
        # Display map if point coordinates are available
        try:
            if 'geometry' in gdf.columns:
                # Create temporary lat/lon columns if geometries are points
                map_df = gdf.copy()
                if map_df.geometry.geom_type.isin(['Point', 'MultiPoint']).any():
                    map_df['lat'] = map_df.geometry.y
                    map_df['lon'] = map_df.geometry.x
                    st.write("### Map Overview")
                    st.map(map_df[['lat', 'lon']].dropna())
        except Exception:
            pass

        st.write("### Data Table Preview")
        # Show dataframe without geometry column for cleaner text display
        st.dataframe(gdf.drop(columns='geometry', errors='ignore'))
        
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
