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

# Set page config
st.set_page_config(
    page_title="Government Department Efficiency Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache data loading function
@st.cache_data
def load_github_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        csv_data = response.content.decode('utf-8')
        return pd.read_csv(StringIO(csv_data))
    except Exception as e:
        st.error(f"Failed to load GitHub data: {e}")
        return None

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
            return pd.DataFrame(data)
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
    github_url = "https://raw.githubusercontent.com/SimpleMobileResponsiveWebsites/department-of-government-efficiency/main/departments.csv"
    departments_df = load_github_data(github_url)
else:
    uploaded_file = st.sidebar.file_uploader("Upload department data file:", type=["csv", "json", "xml"])
    departments_df = parse_uploaded_file(uploaded_file)

# Initialize session state
if 'total_weight' not in st.session_state:
    st.session_state.total_weight = 0

# Define efficiency categories
efficiency_categories = {
    "Operational Efficiency": {
        "Process Optimization": 0,
        "Resource Utilization": 0,
        "Service Delivery Speed": 0,
        "Digital Transformation": 0
    },
    "Fiscal Efficiency": {
        "Budget Management": 0,
        "Cost Control": 0,
        "Resource Allocation": 0,
        "Financial Transparency": 0
    },
    "Administrative Efficiency": {
        "Paperwork Processing": 0,
        "Response Time": 0,
        "Staff Productivity": 0,
        "Regulatory Compliance": 0
    },
    "Public Service Efficiency": {
        "Citizen Satisfaction": 0,
        "Service Accessibility": 0,
        "Communication Effectiveness": 0,
        "Public Engagement": 0
    }
}

# Utility Functions
def calculate_efficiency_score(employees, budget, utilization, oversight, num_regulations, economic_oversight, effectiveness_score):
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
    return (communication + transparency + responsiveness + policy_impact + citizen_satisfaction) / 5 * 20

# Export Functions
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

# Main Assessment Interface
tab1, tab2 = st.tabs(["Metric Assessment", "Detailed Department Data"])

# Department selection for both tabs
if departments_df is not None:
    department_list = departments_df['department_name'].tolist() if 'department_name' in departments_df.columns else []
else:
    department_list = ["Department of Public Works"]  # Default fallback

with tab1:
    st.header("Department Selection")
    selected_department_tab1 = st.selectbox(
        "Select Department for Assessment",
        department_list,
        key="dept_select_tab1"
    )
    
    # Rest of tab1 code...
    st.header("Efficiency Metrics")
    cols = st.columns(len(efficiency_categories))
    
    category_totals = {}
    
    for idx, (category, metrics) in enumerate(efficiency_categories.items()):
        with cols[idx]:
            st.subheader(category)
            category_total = 0
            
            for metric, _ in metrics.items():
                value = st.slider(
                    f"{metric}",
                    min_value=0,
                    max_value=25,
                    value=0,
                    help=f"Rate {metric} from 0-25",
                    key=f"{category}_{metric}"
                )
                efficiency_categories[category][metric] = value
                category_total += value
            
            category_totals[category] = category_total
            st.metric(f"Total {category}", f"{category_total}%")

    # Calculate overall efficiency
    total_efficiency = sum(category_totals.values()) / 4
    st.header("Overall Department Efficiency")
    st.metric("Overall Efficiency Score", f"{total_efficiency:.1f}%")

    # Visualizations
    st.header("Efficiency Visualizations")
    col1, col2 = st.columns(2)

    # Radar Chart
    with col1:
        categories = list(category_totals.keys())
        values = list(category_totals.values())
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself'
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            title="Efficiency Radar Chart"
        )
        st.plotly_chart(fig)

    # Bar Chart
    with col2:
        metrics_data = []
        for category, metrics in efficiency_categories.items():
            for metric, value in metrics.items():
                metrics_data.append({
                    "Category": category,
                    "Metric": metric,
                    "Value": value
                })
        
        df_metrics = pd.DataFrame(metrics_data)
        fig = px.bar(
            df_metrics,
            x="Value",
            y="Metric",
            color="Category",
            title="Detailed Metrics Breakdown",
            orientation='h'
        )
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig)

with tab2:
    st.header("Department Selection")
    selected_department_tab2 = st.selectbox(
        "Select Department for Detailed Data",
        department_list,
        key="dept_select_tab2"
    )
    
    # Rest of tab2 code...
    st.header("Enter Detailed Department Data")
    
    # Basic Information
    department_name = st.text_input("Department Name", value=selected_department_tab2)
    department_desc = st.text_area("Description of the Department", value="Handles infrastructure and public works projects.")
    employees = st.number_input("Number of Employees", min_value=1, value=500)
    
    # Governance Information
    current_governance = st.text_area("Current Areas of Governance", value="Road maintenance, public parks, waste management.")
    suggested_governance = st.text_area("Suggested Areas of Governance", value="Renewable energy infrastructure, smart city development.")
    
    # Governing Regulations
    st.subheader("Governing Regulations")
    num_regulations = st.number_input("Number of regulations", min_value=0, value=3)
    regulations = []
    for i in range(num_regulations):
        regulations.append(st.text_input(f"Regulation {i + 1}", value=f"Regulation {i + 1}"))
    
    # Budget and Oversight
    col1, col2 = st.columns(2)
    with col1:
        budget = st.number_input("Annual Budget (in Million USD)", min_value=0.0, value=100.0)
        utilization = st.slider("Budget Utilization (%)", 0, 100, 75)
    with col2:
        oversight = st.slider("Regulatory Oversight Level", 0, 100, 50)
        economic_oversight = st.slider("Economic Oversight Level", 0, 100, 50)
    
    # Qualitative Assessment
    st.subheader("Qualitative Assessment")
    qual_metrics = ["Communication", "Transparency", "Responsiveness", "Policy Impact", "Citizen Satisfaction"]
    qual_scores = {}
    for metric in qual_metrics:
        qual_scores[metric] = st.select_slider(
            metric,
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: ["Very Poor", "Poor", "Average", "Good", "Excellent"][x-1]
        )

    effectiveness_score = calculate_effectiveness_score(
        qual_scores["Communication"],
        qual_scores["Transparency"],
        qual_scores["Responsiveness"],
        qual_scores["Policy Impact"],
        qual_scores["Citizen Satisfaction"]
    )

    efficiency_score = calculate_efficiency_score(
        employees, budget, utilization, oversight,
        num_regulations, economic_oversight, effectiveness_score
    )

    # Prepare export data
    export_data = {
        "Department Name": department_name,
        "Description": department_desc,
        "Employees": employees,
        "Current Governance": current_governance,
        "Suggested Governance": suggested_governance,
        "Regulations": ", ".join(regulations),
        "Budget (Million USD)": budget,
        "Budget Utilization (%)": utilization,
        "Regulatory Oversight (%)": oversight,
        "Economic Oversight (%)": economic_oversight,
        "Effectiveness Score": effectiveness_score,
        "Efficiency Score": efficiency_score,
        "Category Scores": category_totals,
        "Detailed Metrics": efficiency_categories
    }

    # Export options
    st.header("Export Options")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "Download as CSV",
            data=convert_to_csv(pd.DataFrame([export_data])),
            file_name="department_efficiency.csv",
            mime="text/csv"
        )
        st.download_button(
            "Download as JSON",
            data=convert_to_json(export_data),
            file_name="department_efficiency.json",
            mime="application/json"
        )
    with col2:
        st.download_button(
            "Download as XML",
            data=convert_to_xml(export_data),
            file_name="department_efficiency.xml",
            mime="application/xml"
        )
        st.download_button(
            "Download as PDF",
            data=convert_to_pdf(export_data),
            file_name="department_efficiency.pdf",
            mime="application/pdf"
        )
