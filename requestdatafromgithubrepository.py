import pandas as pd
import streamlit as st
import requests

# GitHub raw file URL
url = "https://raw.githubusercontent.com/SimpleMobileResponsiveWebsites/department-of-government-effiency-app-version-1/main/agenices_list_1.csv"

# Fetch and load the CSV file from GitHub
@st.cache
def load_github_csv(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    csv_data = response.content.decode('utf-8')
    return pd.read_csv(pd.compat.StringIO(csv_data))

# Load the GitHub CSV into a DataFrame
github_data = load_github_csv(url)

# Display a dropdown for selecting an agency or department
st.write("Choose an Agency or Department")
selected_agency = st.selectbox(
    "Select from the list:",
    github_data['Agency or Department Name']  # Adjust the column name based on your CSV structure
)

# Save the user's selection to the application state
if 'selected_agency' not in st.session_state:
    st.session_state.selected_agency = None

st.session_state.selected_agency = selected_agency

# Display the user's selection
st.write(f"Selected Agency: {st.session_state.selected_agency}")
