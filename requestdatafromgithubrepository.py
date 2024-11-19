import pandas as pd
import streamlit as st
import requests
import json
import xml.etree.ElementTree as ET
from io import StringIO

# Set page configuration
st.set_page_config(
    page_title="Government Department Efficiency Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Utility function to fetch and load CSV from GitHub
@st.cache_data
def load_github_csv(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    csv_data = response.content.decode('utf-8')
    return pd.read_csv(StringIO(csv_data))

# Sidebar for file uploads
st.sidebar.header("Upload Data for Efficiency Calculator")
uploaded_file = st.sidebar.file_uploader(
    "Upload a .csv, .json, or .xml file:",
    type=["csv", "json", "xml"]
)

# Parse uploaded files
def parse_uploaded_file(file):
    if file is None:
        return None
    try:
        file_extension = file.name.split('.')[-1].lower()
        if file_extension == "csv":
            df = pd.read_csv(file)
            st.sidebar.success("CSV file loaded successfully")
            return df
        elif file_extension == "json":
            data = json.load(file)
            st.sidebar.success("JSON file loaded successfully")
            return pd.DataFrame(data)  # Convert JSON to DataFrame
        elif file_extension == "xml":
            tree = ET.parse(file)
            root = tree.getroot()
            data = [{child.tag: child.text for child in element} for element in root]
            st.sidebar.success("XML file loaded successfully")
            return pd.DataFrame(data)
        else:
            st.sidebar.error("Unsupported file format")
            return None
    except Exception as e:
        st.sidebar.error(f"Failed to load file: {e}")
        return None

# Load GitHub data or user-uploaded data
github_url = "https://raw.githubusercontent.com/SimpleMobileResponsiveWebsites/department-of-government-effiency-app-version-1/main/agenices_list_1.csv"
github_data = load_github_csv(github_url)
uploaded_data = parse_uploaded_file(uploaded_file)

# Use uploaded data if available; fallback to GitHub data
data_frame = uploaded_data if uploaded_data is not None else github_data

# Display a dropdown for selecting an agency or department
st.title("Government Department Efficiency Calculator")
if data_frame is not None:
    st.write("Loaded Data Preview:")
    st.dataframe(data_frame)

    # Ensure a valid column for dropdown
    dropdown_column = st.selectbox(
        "Select a column for the dropdown menu:",
        data_frame.columns
    )

    selected_agency = st.selectbox(
        "Choose an Agency or Department:",
        data_frame[dropdown_column].dropna().unique()  # Remove NaN values
    )

    # Save the user's selection to the application state
    if 'selected_agency' not in st.session_state:
        st.session_state.selected_agency = None

    st.session_state.selected_agency = selected_agency

    # Display the user's selection
    st.write(f"Selected Agency: {st.session_state.selected_agency}")
else:
    st.warning("Please upload a file or use the default GitHub data.")
