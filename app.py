import json
import pandas as pd
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Dataset Viewer - Special Economic Zones",
    page_icon="🌍",
    layout="wide",
)


# Load the full JSON data from file
@st.cache_data
def load_data():
  try:
    with open("dataset.json", "r", encoding="utf-8") as f:
      return json.load(f)
  except FileNotFoundError:
    st.error(
        "⚠️ 'dataset.json' not found. Please make sure the file is in the same"
        " directory."
    )
    return None


data = load_data()

if data:
  # Dashboard Header
  st.title(f"🌍 {data.get('name', 'Dataset Viewer')}")
  st.markdown("---")

  # Sidebar for Navigation
  st.sidebar.title("Navigation")
  section = st.sidebar.radio(
      "Go to",
      [
          "Overview",
          "Identification & Metadata",
          "Geographical Coverage",
          "Raw JSON Viewer",
      ],
  )

  if section == "Overview":
    st.header("Dataset Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Status", data.get("status"))
    col2.metric("Version", data.get("version_number"))
    col3.metric("Dataset ID", data.get("dataset_unique_id"))

    st.subheader("Description")
    desc = data.get("identification", {}).get("description", "")
    st.markdown(desc, unsafe_allow_html=True)

    st.subheader("Quick Links")
    legacy_url = data.get("app_legacy_url")
    if legacy_url:
      st.markdown(f"🔗 [View Original Datacatalog Entry]({legacy_url})")

  elif section == "Identification & Metadata":
    st.header("Identification Metadata")
    ident = data.get("identification", {})

    st.text_input("Title", ident.get("title", ""))
    st.text_input("Acronym", ident.get("acronym", ""))
    st.text_input(
        "Practice Name", ident.get("practice", {}).get("name", "")
    )
    st.text_input("Work Unit", ident.get("work_unit", {}).get("name", ""))

    st.subheader("Point of Contact / Team Members")
    contacts = ident.get("point_of_contact", [])
    if contacts:
      st.dataframe(pd.DataFrame(contacts), use_container_width=True)

  elif section == "Geographical Coverage":
    st.header("Geographical Extent & Coverage")
    geo_coverage = data.get("geographical_extent", {}).get("coverage", [])

    st.info(f"Total coverage regions/countries listed: {len(geo_coverage)}")

    if geo_coverage:
      df_geo = pd.DataFrame(geo_coverage)
      # Search bar for countries
      search_term = st.text_input("🔍 Search country or region:")
      if search_term:
        df_geo = df_geo[
            df_geo["name"].str.contains(search_term, case=False, na=False)
        ]

      st.dataframe(df_geo[["code", "name"]], use_container_width=True)

  elif section == "Raw JSON Viewer":
    st.header("Raw JSON Data")
    st.json(data)
