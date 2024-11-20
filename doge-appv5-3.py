import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import xml.etree.ElementTree as ET
import requests
from io import BytesIO, StringIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(message)s")

# Set page configuration
st.set_page_config(
    page_title="Government Department Efficiency Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Default data in case of GitHub failure
DEFAULT_DATA = pd.DataFrame({
    "department_name": ["Department of Public Works", "Health and Human Services"],
    "category": ["Public Services", "Healthcare"]
})

# Cache data loading function
@st.cache_data
def load_github_data(url):
    """Load data from a GitHub URL or return default data on failure."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        csv_data = response.content.decode('utf-8')
        return pd.read_csv(StringIO(csv_data))
    except requests.exceptions.RequestException as e:
        logging.error(f"GitHub data load error: {e}")
        st.error("Failed to load GitHub data. Using default dataset.")
        return DEFAULT_DATA

# Parse uploaded files
def parse_uploaded_file(file):
    """Parse uploaded file and return a DataFrame."""
    if file is None:
        return None
    try:
        file_extension = file.name.split('.')[-1].lower()
        if file_extension == "csv":
            return pd.read_csv(file)
        elif file_extension == "json":
            data = json.load(file)
            return pd.DataFrame(data)
        elif file_extension == "xml":
            tree = ET.parse(file)
            root = tree.getroot()
            data = [{child.tag: child.text for child in element} for element in root]
            return pd.DataFrame(data)
        else:
            st.sidebar.error("Unsupported file format")
            return None
    except Exception as e:
        st.sidebar.error(f"Failed to load file: {e}")
        return None

# Utility functions for calculations
def calculate_efficiency_score(employees, budget, utilization, oversight, num_regulations, economic_oversight, effectiveness_score):
    """Calculate department efficiency score."""
    score = (
        (utilization * 0.3) +
        ((100 - oversight) * 0.2) +
        (min(2000 / employees, 100) * 0.2) +
        (max(100 - num_regulations * 2, 0) * 0.15) +
        (100 - economic_oversight * 0.15) +
        (effectiveness_score * 0.5)
    )
    return min(score / 1.5, 100)

def calculate_effectiveness_score(communication, transparency, responsiveness, policy_impact, citizen_satisfaction):
    """Calculate effectiveness score based on qualitative metrics."""
    return (communication + transparency + responsiveness + policy_impact + citizen_satisfaction) / 5 * 20

# Export functions
def convert_to_csv(data):
    return data.to_csv(index=False).encode('utf-8')

def convert_to_json(data):
    return json.dumps(data, indent=4).encode('utf-8')

def convert_to_xml(data):
    root = ET.Element("DepartmentData")
    for key, value in data.items():
        child = ET.SubElement(root, key)
        child.text = str(value)
    return ET.tostring(root, encoding='utf-8')

def convert_to_pdf(data):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica", 12)
    y_position = 750
    for key, value in data.items():
        text_line = f"{key}: {value}"
        p.drawString(30, y_position, text_line)
        y_position -= 20
    p.save()
    buffer.seek(0)
    return buffer

# Title and description
st.title("Government Department Efficiency Calculator")
st.markdown("""
This application helps assess and visualize the efficiency of government departments.  
Rate each component based on current department performance and governance metrics.
""")

# Sidebar for data source selection
st.sidebar.header("Data Source Configuration")
data_source = st.sidebar.radio("Select Data Source:", ["GitHub Repository", "File Upload"])

if data_source == "GitHub Repository":
    github_url = "https://raw.githubusercontent.com/SimpleMobileResponsiveWebsites/department-of-government-effiency-app-version-1/main/downloaded_data%20(5).csv"
    departments_df = load_github_data(github_url)
else:
    uploaded_file = st.sidebar.file_uploader("Upload department data file:", type=["csv", "json", "xml"])
    departments_df = parse_uploaded_file(uploaded_file)

# Handle department data
if departments_df is not None and not departments_df.empty:
    department_list = departments_df['department_name'].tolist()
else:
    department_list = ["Default Department"]  # Fallback

# Main assessment interface
tab1, tab2 = st.tabs(["Metric Assessment", "Detailed Department Data"])

# Metric Assessment Tab
with tab1:
    st.header("Department Selection")
    selected_department_tab1 = st.selectbox("Select Department for Assessment", department_list, key="dept_select_tab1")

    st.header("Efficiency Metrics")
    cols = st.columns(len(efficiency_categories := {
        "Operational Efficiency": {"Process Optimization": 0, "Resource Utilization": 0, "Service Delivery Speed": 0, "Digital Transformation": 0},
        "Fiscal Efficiency": {"Budget Management": 0, "Cost Control": 0, "Resource Allocation": 0, "Financial Transparency": 0},
        "Administrative Efficiency": {"Paperwork Processing": 0, "Response Time": 0, "Staff Productivity": 0, "Regulatory Compliance": 0},
        "Public Service Efficiency": {"Citizen Satisfaction": 0, "Service Accessibility": 0, "Communication Effectiveness": 0, "Public Engagement": 0}
    }))
    category_totals = {}

    for idx, (category, metrics) in enumerate(efficiency_categories.items()):
        with cols[idx]:
            st.subheader(category)
            category_total = 0
            for metric, _ in metrics.items():
                value = st.slider(f"{metric}", min_value=0, max_value=25, value=0, help=f"Rate {metric} from 0-25", key=f"{category}_{metric}")
                efficiency_categories[category][metric] = value
                category_total += value
            category_totals[category] = category_total
            st.metric(f"Total {category}", f"{category_total}%")

    total_efficiency = sum(category_totals.values()) / 4
    st.header("Overall Department Efficiency")
    st.metric("Overall Efficiency Score", f"{total_efficiency:.1f}%")

    st.header("Efficiency Visualizations")
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure(data=go.Scatterpolar(r=list(category_totals.values()), theta=list(category_totals.keys()), fill='toself'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, title="Efficiency Radar Chart")
        st.plotly_chart(fig)

    with col2:
        metrics_data = [{"Category": cat, "Metric": met, "Value": val} for cat, mets in efficiency_categories.items() for met, val in mets.items()]
        fig = px.bar(pd.DataFrame(metrics_data), x="Value", y="Metric", color="Category", orientation="h", title="Detailed Metrics Breakdown")
        fig.update_layout(yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(fig)

# Detailed Department Data Tab
with tab2:
    st.header("Department Selection")
    selected_department_tab2 = st.selectbox("Select Department for Detailed Data", department_list, key="dept_select_tab2")
    
    st.header("Enter Detailed Department Data")
    department_name = st.text_input("Department Name", value=selected_department_tab2)
    department_desc = st.text_area("Description of the Department", value="Handles infrastructure and public works projects.")
    employees = st.number_input("Number of Employees", min_value=1, value=500)
    current_governance = st.text_area("Current Areas of Governance", value="Road maintenance, public parks, waste management.")
    suggested_governance = st.text_area("Suggested Areas of Governance", value="Renewable energy infrastructure, smart city development.")
    num_regulations = st.number_input("Number of regulations", min_value=0, value=3)
    regulations = [st.text_input(f"Regulation {i + 1}", value=f"Regulation {i + 1}") for i in range(num_regulations)]

    export_data = {
        "Department Name": department_name,
        "Description": department_desc,
        "Number of Employees": employees,
        "Current Governance Areas": current_governance,
        "Suggested Governance Areas": suggested_governance,
        "Number of Regulations": num_regulations,
        "Regulations": regulations
    }

    col1, col2 = st.columns(2)
    with col1:
        csv_data = convert_to_csv(pd.DataFrame([export_data]))
        st.download_button("Download as CSV", data=csv_data, file_name="department_data.csv")
        json_data = convert_to_json(export_data)
        st.download_button("Download as JSON", data=json_data, file_name="department_data.json")

    with col2:
        xml_data = convert_to_xml(export_data)
        st.download_button("Download as XML", data=xml_data, file_name="department_data.xml")
        pdf_data = convert_to_pdf(export_data)
        st.download_button("Download as PDF", data=pdf_data, file_name="department_data.pdf", mime="application/pdf")
