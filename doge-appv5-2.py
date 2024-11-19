import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import xml.etree.ElementTree as ET
import requests
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from base64 import b64decode

# Set page config
st.set_page_config(
    page_title="Government Department Efficiency Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Section for File Upload
st.sidebar.header("Upload Data for Efficiency Calculator")
uploaded_file = st.sidebar.file_uploader(
    "Upload a .csv, .json, or .xml file:",
    type=["csv", "json", "xml"]
)

# GitHub Data Loading Functions
def fetch_github_raw_file(file_path):
    """Fetch raw file content from GitHub repository"""
    base_url = "https://raw.githubusercontent.com/SimpleMobileResponsiveWebsites/department-of-government-effiencyapp-version-1/main/"
    response = requests.get(base_url + file_path)
    if response.status_code == 200:
        return response.text
    return None

# Parse the uploaded file
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

# Process uploaded file
data_frame = parse_uploaded_file(uploaded_file)

# GitHub Data Section
def add_github_data_section():
    st.sidebar.header("Load Saved Department Data")

    file_options = {
        "CSV Format": "department_efficiency.csv",
        "JSON Format": "department_efficiency.json",
        "XML Format": "department_efficiency.xml",
        "PDF Format": "department_efficiency.pdf"
    }

    selected_format = st.sidebar.selectbox(
        "Select file format to load",
        options=list(file_options.keys())
    )

    if st.sidebar.button("Load Data"):
        file_name = file_options[selected_format]
        file_content = fetch_github_raw_file(file_name)

        if file_content:
            try:
                if selected_format == "CSV Format":
                    df = pd.read_csv(BytesIO(file_content.encode()))
                    st.sidebar.success("CSV data loaded successfully")
                    return df
                elif selected_format == "JSON Format":
                    data = json.loads(file_content)
                    st.sidebar.success("JSON data loaded successfully")
                    return pd.DataFrame(data)
                elif selected_format == "XML Format":
                    root = ET.fromstring(file_content)
                    data = {child.tag: child.text for child in root}
                    st.sidebar.success("XML data loaded successfully")
                    return pd.DataFrame([data])
                elif selected_format == "PDF Format":
                    st.sidebar.warning("PDF preview not available. Click below to download.")
                    st.sidebar.download_button(
                        "Download PDF",
                        file_content.encode(),
                        file_name=file_options[selected_format],
                        mime="application/pdf"
                    )
                    return None
            except Exception as e:
                st.sidebar.error(f"Error loading file: {str(e)}")
        else:
            st.sidebar.error("Failed to load file from repository")

    return None

# Load GitHub data if no uploaded file
loaded_data = add_github_data_section()
if loaded_data is not None and data_frame is None:
    data_frame = loaded_data

# Title and Dropdown
st.title("Government Department Efficiency Calculator")

if data_frame is not None:
    st.write("Loaded Data Preview:")
    st.dataframe(data_frame)

    # Ensure a valid column for dropdown
    dropdown_column = st.selectbox(
        "Select a column for the dropdown menu:",
        data_frame.columns
    )

    selected_value = st.selectbox(
        "Choose an Agency or Department:",
        data_frame[dropdown_column].dropna().unique()  # Remove NaN values
    )

    # Display the selected value
    st.write(f"Selected Agency or Department: {selected_value}")
else:
    st.warning("Please upload a file or load data to populate the dropdown menu.")

# Rest of the page content...
st.markdown("""
This application helps assess and visualize the efficiency of government departments.
Rate each component based on current department performance and governance metrics.
""")
