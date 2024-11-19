# import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import json
import xml.etree.ElementTree as ET
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Government Agencies Dataset
agency_data = [
    {"Agency Name": "Access Board U.S.", "Type": "Independent Agency", "Parent Department": "", "Category": "Regulatory", "Acronym": "USAB"},
    {"Agency Name": "Administration for Children and Families", "Type": "Sub-Agency", "Parent Department": "Health and Human Services", "Category": "Social Services", "Acronym": "ACF"},
    {"Agency Name": "Administration for Community Living", "Type": "Sub-Agency", "Parent Department": "Health and Human Services", "Category": "Social Services", "Acronym": "ACL"},
    {"Agency Name": "Amtrak", "Type": "Government Corporation", "Parent Department": "", "Category": "Transportation", "Acronym": "AMTRAK"},
    {"Agency Name": "Bureau of Labor Statistics", "Type": "Sub-Agency", "Parent Department": "Labor", "Category": "Statistics", "Acronym": "BLS"},
    {"Agency Name": "Department of Justice", "Type": "Cabinet Department", "Parent Department": "", "Category": "Justice", "Acronym": "DOJ"},
    {"Agency Name": "Environmental Protection Agency", "Type": "Independent Agency", "Parent Department": "", "Category": "Environmental", "Acronym": "EPA"},
    {"Agency Name": "Federal Aviation Administration", "Type": "Sub-Agency", "Parent Department": "Transportation", "Category": "Transportation", "Acronym": "FAA"},
    {"Agency Name": "NASA", "Type": "Independent Agency", "Parent Department": "", "Category": "Space", "Acronym": "NASA"},
    {"Agency Name": "Social Security Administration", "Type": "Independent Agency", "Parent Department": "", "Category": "Social Services", "Acronym": "SSA"}
]

# Convert to DataFrame
agency_df = pd.DataFrame(agency_data)

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

# Convert data to CSV
def convert_to_csv(data):
    return data.to_csv(index=False).encode('utf-8')

# Convert data to JSON
def convert_to_json(data):
    return json.dumps(data, indent=4).encode('utf-8')

# Convert data to XML
def convert_to_xml(data):
    root = ET.Element("AgencyData")
    for index, row in data.iterrows():
        agency = ET.SubElement(root, "Agency")
        for col in data.columns:
            child = ET.SubElement(agency, col)
            child.text = str(row[col])
    return ET.tostring(root, encoding='utf-8')

# Convert data to PDF
def convert_to_pdf(data):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica", 10)
    y_position = 750
    p.drawString(30, y_position, "Government Agencies Report")
    y_position -= 20
    for index, row in data.iterrows():
        text = f"{row['Agency Name']} ({row['Acronym']}): {row['Type']}, {row['Category']}"
        p.drawString(30, y_position, text)
        y_position -= 15
        if y_position < 50:
            p.showPage()
            y_position = 750
    p.save()
    buffer.seek(0)
    return buffer

# Input detailed department data
def input_detailed_data():
    st.header("Government Agencies Data")
    st.dataframe(agency_df)

# Download dataset
def download_agency_data():
    st.header("Download Government Agencies Dataset")
    csv_data = convert_to_csv(agency_df)
    json_data = convert_to_json(agency_df.to_dict(orient='records'))
    xml_data = convert_to_xml(agency_df)
    pdf_data = convert_to_pdf(agency_df)

    st.download_button("Download as CSV", data=csv_data, file_name="agencies.csv", mime="text/csv")
    st.download_button("Download as JSON", data=json_data, file_name="agencies.json", mime="application/json")
    st.download_button("Download as XML", data=xml_data, file_name="agencies.xml", mime="application/xml")
    st.download_button("Download as PDF", data=pdf_data, file_name="agencies.pdf", mime="application/pdf")

# Main function
def main():
    st.sidebar.title("Navigation")
    option = st.sidebar.radio("Select a Section", ["Agency Data", "Download Agency Report"])
    
    if option == "Agency Data":
        input_detailed_data()
    elif option == "Download Agency Report":
        download_agency_data()

if __name__ == "__main__":
    main()
