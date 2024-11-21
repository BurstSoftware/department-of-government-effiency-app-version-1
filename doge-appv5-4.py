import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import xml.etree.ElementTree as ET
from io import BytesIO, StringIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import requests

# Set page config
st.set_page_config(
    page_title="Government Department Efficiency Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'total_weight' not in st.session_state:
    st.session_state.total_weight = 0
if 'selected_agency' not in st.session_state:
    st.session_state.selected_agency = None

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

# File parsing functions
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
            data = [{child.tag: child.text for child in element}
                    for element in root]
            st.sidebar.success("XML file loaded successfully")
            return pd.DataFrame(data)
        else:
            st.sidebar.error("Unsupported file format")
            return None
    except Exception as e:
        st.sidebar.error(f"Failed to load file: {e}")
        return None

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

# Sidebar for data upload
st.sidebar.header("Upload Data for Efficiency Calculator")
uploaded_file = st.sidebar.file_uploader(
    "Upload a .csv, .json, or .xml file:",
    type=["csv", "json", "xml"]
)

# Load default data
github_url = "https://raw.githubusercontent.com/SimpleMobileResponsiveWebsites/department-of-government-effiency-app-version-1/main/agenices_list_1.csv"
@st.cache_data
def load_github_csv(url):
    response = requests.get(url)
    response.raise_for_status()
    csv_data = response.content.decode('utf-8')
    return pd.read_csv(StringIO(csv_data))

github_data = load_github_csv(github_url)
uploaded_data = parse_uploaded_file(uploaded_file)
data_frame = uploaded_data if uploaded_data is not None else github_data

# Main interface
st.title("Government Department Efficiency Calculator")

if data_frame is not None:
    st.write("Loaded Data Preview:")
    st.dataframe(data_frame)

    # Department selection
    dropdown_column = st.selectbox(
        "Select a column for the dropdown menu:",
        data_frame.columns
    )
    selected_agency = st.selectbox(
        "Choose an Agency or Department:",
        data_frame[dropdown_column].dropna().unique()
    )
    st.session_state.selected_agency = selected_agency

    # Main tabs
    tab1, tab2 = st.tabs(["Metric Assessment", "Detailed Department Data"])

    with tab1:
        st.header("Efficiency Metrics")
        cols = st.columns(len(efficiency_categories))
        category_totals = {}

        # Create sliders for each category
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

        # Calculate and display overall efficiency
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
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig)

    with tab2:
        st.header("Enter Detailed Department Data")

        # Basic Information
        department_name = st.text_input("Department Name", value=selected_agency)
        department_desc = st.text_area("Description of the Department", value="")
        employees = st.number_input("Number of Employees", min_value=1, value=500)

        # Governance Information
        current_governance = st.text_area("Current Areas of Governance", value="")
        suggested_governance = st.text_area("Suggested Areas of Governance", value="")

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
            economic_oversight = st.slider("Economic Oversight Level", 0, 100, 30)

        # Effectiveness Score
        st.subheader("Effectiveness Metrics")
        communication = st.slider("Communication", 0, 100, 70)
        transparency = st.slider("Transparency", 0, 100, 80)
        responsiveness = st.slider("Responsiveness", 0, 100, 85)
        policy_impact = st.slider("Policy Impact", 0, 100, 75)
        citizen_satisfaction = st.slider("Citizen Satisfaction", 0, 100, 90)

        effectiveness_score = calculate_effectiveness_score(
            communication, transparency, responsiveness, policy_impact, citizen_satisfaction
        )

        st.metric("Effectiveness Score", f"{effectiveness_score:.1f}")

        # Efficiency Calculation
        efficiency_score = calculate_efficiency_score(
            employees, budget, utilization, oversight, num_regulations,
            economic_oversight, effectiveness_score
        )

        st.metric("Calculated Efficiency Score", f"{efficiency_score:.1f}")

    # Export Options
    st.header("Export Data")
    export_format = st.selectbox("Select export format", ["CSV", "JSON", "XML", "PDF"])
    export_data = {
        "Department Name": department_name,
        "Efficiency Score": efficiency_score,
        "Effectiveness Score": effectiveness_score,
        "Number of Employees": employees,
        "Budget (Million USD)": budget
    }

    if st.button("Export Data"):
        if export_format == "CSV":
            st.download_button(
                "Download CSV",
                data=convert_to_csv(pd.DataFrame([export_data])),
                file_name="department_data.csv",
                mime="text/csv"
            )
        elif export_format == "JSON":
            st.download_button(
                "Download JSON",
                data=convert_to_json(export_data),
                file_name="department_data.json",
                mime="application/json"
            )
        elif export_format == "XML":
            st.download_button(
                "Download XML",
                data=convert_to_xml(export_data),
                file_name="department_data.xml",
                mime="application/xml"
            )
        elif export_format == "PDF":
            pdf_file = convert_to_pdf(export_data)
            st.download_button(
                "Download PDF",
                data=pdf_file,
                file_name="department_data.pdf",
                mime="application/pdf"
            )
