import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import json
import xml.etree.ElementTree as ET
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Function to calculate efficiency score
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

# Calculate qualitative effectiveness score
def calculate_effectiveness_score(communication, transparency, responsiveness, policy_impact, citizen_satisfaction):
    return (communication + transparency + responsiveness + policy_impact + citizen_satisfaction) / 5 * 20

# Convert input data to CSV
def convert_to_csv(data):
    return data.to_csv(index=False).encode('utf-8')

# Convert input data to JSON
def convert_to_json(data):
    return json.dumps(data, indent=4).encode('utf-8')

# Convert input data to XML
def convert_to_xml(data):
    root = ET.Element("DepartmentData")
    for key, value in data.items():
        child = ET.SubElement(root, key)
        child.text = str(value)
    return ET.tostring(root, encoding='utf-8')

# Convert input data to PDF
def convert_to_pdf(data):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica", 12)
    text = f"Department Efficiency Report\n\n"
    y_position = 750
    for key, value in data.items():
        text_line = f"{key}: {value}"
        p.drawString(30, y_position, text_line)
        y_position -= 20
    p.save()
    buffer.seek(0)
    return buffer

# Input detailed department data
def input_detailed_data():
    st.header("Enter Detailed Department Data")

    # Basic Information
    department_name = st.text_input("Department Name", value="Department of Public Works")
    department_desc = st.text_area("Description of the Department", value="Handles infrastructure and public works projects.")
    employees = st.number_input("Number of Employees", min_value=1, value=500)

    # Governance Information
    current_governance = st.text_area("Current Areas of Governance", value="Road maintenance, public parks, waste management.")
    suggested_governance = st.text_area("Suggested Areas of Governance", value="Renewable energy infrastructure, smart city development.")
    
    # Governing Regulations
    st.subheader("Governing Regulations in Place Today")
    regulations = []
    num_regulations = st.number_input("How many regulations does this department currently enforce?", min_value=0, value=3)
    
    for i in range(num_regulations):
        regulation = st.text_input(f"Regulation {i + 1}", value=f"Regulation {i + 1}")
        regulations.append(regulation)
    
    # Budget and Oversight
    budget = st.number_input("Annual Budget (in Million USD)", min_value=0.0, value=100.0)
    utilization = st.slider("Budget Utilization (%)", 0, 100, 75)
    oversight = st.slider("Regulatory Oversight Level (0-100)", 0, 100, 50)
    economic_oversight = st.slider("Economic Oversight Level (0-100)", 0, 100, 50)

    # Qualitative Assessment
    communication = st.select_slider("Communication Effectiveness", options=[1, 2, 3, 4, 5], format_func=lambda x: ["Very Poor", "Poor", "Average", "Good", "Excellent"][x-1])
    transparency = st.select_slider("Transparency", options=[1, 2, 3, 4, 5], format_func=lambda x: ["Very Poor", "Poor", "Average", "Good", "Excellent"][x-1])
    responsiveness = st.select_slider("Responsiveness", options=[1, 2, 3, 4, 5], format_func=lambda x: ["Very Poor", "Poor", "Average", "Good", "Excellent"][x-1])
    policy_impact = st.select_slider("Policy Impact", options=[1, 2, 3, 4, 5], format_func=lambda x: ["Very Poor", "Poor", "Average", "Good", "Excellent"][x-1])
    citizen_satisfaction = st.select_slider("Citizen Satisfaction", options=[1, 2, 3, 4, 5], format_func=lambda x: ["Very Poor", "Poor", "Average", "Good", "Excellent"][x-1])

    effectiveness_score = calculate_effectiveness_score(communication, transparency, responsiveness, policy_impact, citizen_satisfaction)
    efficiency_score = calculate_efficiency_score(employees, budget, utilization, oversight, num_regulations, economic_oversight, effectiveness_score)

    st.success(f"The calculated efficiency score for the {department_name} is: {efficiency_score:.2f}%")

    # Prepare data for export
    input_data = {
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
        "Efficiency Score": efficiency_score
    }

    data_df = pd.DataFrame([input_data])

    # Download Options
    st.subheader("Download Enhanced Report")
    csv_data = convert_to_csv(data_df)
    json_data = convert_to_json(input_data)
    xml_data = convert_to_xml(input_data)
    pdf_data = convert_to_pdf(input_data)

    st.download_button("Download as CSV", data=csv_data, file_name="efficiency_report.csv", mime="text/csv")
    st.download_button("Download as JSON", data=json_data, file_name="efficiency_report.json", mime="application/json")
    st.download_button("Download as XML", data=xml_data, file_name="efficiency_report.xml", mime="application/xml")
    st.download_button("Download as PDF", data=pdf_data, file_name="efficiency_report.pdf", mime="application/pdf")

# Main function
def main():
    st.sidebar.title("Navigation")
    option = st.sidebar.radio("Select a Section", ["Input Data", "Download Report"])
    if option == "Input Data":
        input_detailed_data()

if __name__ == "__main__":
    main()
