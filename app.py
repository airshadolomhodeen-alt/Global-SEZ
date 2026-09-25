import folium
import pandas as pd
import requests
import streamlit as st
from streamlit_folium import st_folium

# Page configuration
st.set_page_config(
    page_title="Global Economic Zones", page_icon="🌍", layout="wide"
)

st.title("🌍 Global Economic Zones Dashboard")
st.markdown(
    "Explore economic zones and their classifications using the interactive map"
    " below."
)


# Optional helper function using your requests snippet
def fetch_sez_page_content():
  url = "https://sezexplorer.org/zones"
  headers = {
      "accept": (
          "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
      ),
      "accept-language": "en-US,en;q=0.9",
      "cache-control": "max-age=0",
      "referer": "https://www.google.com/",
      "user-agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/153.0.0.0 Safari/537.36"
      ),
  }
  try:
    response = requests.get(url, headers=headers, timeout=10)
    if "text/html" in response.headers.get("content-type", ""):
      with open("sez_page.html", "w", encoding="utf-8") as f:
        f.write(response.text)
      return True
  except Exception as e:
    print(f"Request error: {e}")
  return False


# 1. Load your economic zones data
@st.cache_data
def load_data():
  zones_df = pd.read_csv("zones.csv")
  return zones_df


try:
  zones_df = load_data()
except FileNotFoundError:
  st.error(
      "❌ 'zones.csv' file not found. Please place your CSV file in the app"
      " directory."
  )
  st.stop()

# 2. Initialize map using Esri World Street Map
m = folium.Map(
    location=[12.8797, 121.7740], zoom_start=6, tiles="Esri.WorldStreetMap"
)

# 3. Define a distinct color palette for your categories
color_palette = [
    "#e41a1c",
    "#377eb8",
    "#4daf4a",
    "#984ea3",
    "#ff7f00",
    "#ffff33",
    "#a65628",
    "#f781bf",
    "#999999",
    "#66c2a5",
    "#fc8d62",
    "#8da0cb",
]

category_column = "NATURE"
unique_categories = (
    zones_df[category_column].dropna().unique()
    if category_column in zones_df.columns
    else []
)

category_colors = {
    cat: color_palette[i % len(color_palette)]
    for i, cat in enumerate(unique_categories)
}

# 4. Add markers with dynamic colors based on their classification
if "lat" in zones_df.columns and "lon" in zones_df.columns:
  for _, row in zones_df.iterrows():
    if pd.isna(row["lat"]) or pd.isna(row["lon"]):
      continue

    category_val = row.get(category_column, "Unknown")
    marker_color = category_colors.get(category_val, "#999999")

    popup_text = f"""
            <b>Zone Name:</b> {row.get('ZONE_NAME', 'N/A')}<br>
            <b>Classification:</b> {category_val}<br>
            <b>Status:</b> {row.get('STATUS', 'N/A')}<br>
            <b>City:</b> {row.get('CITY', 'N/A')}
        """

    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=6,
        color=marker_color,
        fill=True,
        fill_color=marker_color,
        fill_opacity=0.85,
        popup=folium.Popup(popup_text, max_width=300),
    ).add_to(m)

# 5. Build a professional HTML legend positioned in the lower right corner
legend_html = """
<div style="
    position: fixed; 
    bottom: 40px; 
    right: 20px; 
    width: 220px; 
    max-height: 180px;
    overflow-y: auto;
    background-color: rgba(255, 255, 255, 0.95); 
    z-index: 9999; 
    font-family: Arial, sans-serif;
    font-size: 11px;
    border: 1px solid #ccc; 
    border-radius: 6px; 
    padding: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
    <p style="margin: 0 0 6px 0; font-weight: bold; font-size: 12px; color: #333; text-align: center; border-bottom: 1px solid #ddd; padding-bottom: 3px;">Zone Classifications</p>
"""

for cat, color in category_colors.items():
  legend_html += f"""
    <div style="display: flex; align-items: center; margin-bottom: 5px;">
        <span style="background: {color}; width: 10px; height: 10px; border-radius: 50%; display: inline-block; margin-right: 6px; flex-shrink: 0;"></span>
        <span style="color: #444; line-height: 1.1; word-break: break-word;">{cat}</span>
    </div>
    """

legend_html += "</div>"

# Add legend and layer control to the map
m.get_root().html.add_child(folium.Element(legend_html))
folium.LayerControl().add_to(m)

# 6. Render the map inside Streamlit
st_folium(m, width=1200, height=600, use_container_width=True)
