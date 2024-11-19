import streamlit as st
import pandas as pd
from datetime import datetime, date
import json

# Define the government structure
government_agencies = {
    "Federal Government": {
        "Executive Branch": {
            "Department of Defense": {
                "Military Services": ["Army", "Navy", "Air Force", "Marines", "Space Force"],
                "Civilian Agencies": ["Defense Intelligence Agency", "National Security Agency"]
            },
            "Department of Homeland Security": ["CBP", "ICE", "Secret Service", "FEMA", "TSA"],
            "Department of State": ["Bureau of Consular Affairs", "Bureau of Diplomatic Security"],
            "Department of Treasury": ["IRS", "US Mint", "Office of Financial Research"],
            "Department of Justice": ["FBI", "DEA", "ATF"]
        },
        "Legislative Branch": {
            "Congress": ["Senate", "House of Representatives"],
            "Support Agencies": ["GAO", "CBO", "Library of Congress"]
        },
        "Judicial Branch": ["Supreme Court", "Court of Appeals", "District Courts"]
    },
    "State Government": {
        "Executive Branch": ["Governor's Office", "Attorney General", "State Agencies"],
        "Legislative Branch": ["State Senate", "State House"],
        "Judicial Branch": ["State Supreme Court", "Appeals Courts", "Trial Courts"]
    }
}

def calculate_efficiency_metrics(efficiency_score, budget_utilization, service_quality, processing_time):
    """Calculate overall efficiency based on multiple metrics"""
    weights = {
        'efficiency_score': 0.3,
        'budget_utilization': 0.3,
        'service_quality': 0.2,
        'processing_time': 0.2
    }
    
    overall_score = (
        efficiency_score * weights['efficiency_score'] +
        budget_utilization * weights['budget_utilization'] +
        service_quality * weights['service_quality'] +
        processing_time * weights['processing_time']
    )
    
    return round(overall_score, 2)

def main():
    st.set_page_config(page_title="Government Efficiency Analyzer", layout="wide")
    
    # Title and description
    st.title("🏛️ Government Efficiency Analyzer")
    st.markdown("""
    This tool helps analyze and track the efficiency of various government agencies 
    across different metrics and organizational levels.
    """)
    
    # Initialize session state for storing agency data
    if 'agency_data' not in st.session_state:
        st.session_state.agency_data = {}
    
    # Create columns for layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Agency Selection")
        
        def create_dropdown(data, level=0):
            if isinstance(data, dict):
                options = list(data.keys())
                key = f"level_{level}"
                selected = st.selectbox(f"Level {level + 1}", options, key=key)
                
                if selected:
                    return create_dropdown(data[selected], level + 1)
                return None
            
            elif isinstance(data, list):
                selected_agency = st.selectbox(f"Level {level + 1}", data)
                return selected_agency
            
            return None
        
        selected_agency = create_dropdown(government_agencies)
    
    with col2:
        if selected_agency:
            st.subheader(f"Efficiency Analysis for: {selected_agency}")
            
            # Create tabs for different aspects of analysis
            tabs = st.tabs(["Basic Information", "Efficiency Metrics", "Performance History"])
            
            # Basic Information Tab
            with tabs[0]:
                description = st.text_area(
                    "Agency Description",
                    value=st.session_state.agency_data.get(selected_agency, {}).get('description', ''),
                    height=100
                )
                
                mandate = st.text_area(
                    "Agency Mandate",
                    value=st.session_state.agency_data.get(selected_agency, {}).get('mandate', ''),
                    height=100
                )
                
                established_date = st.date_input(
                    "Date Established",
                    value=datetime.strptime(
                        st.session_state.agency_data.get(selected_agency, {}).get('established_date', '2000-01-01'),
                        '%Y-%m-%d'
                    ).date() if selected_agency in st.session_state.agency_data else date(2000, 1, 1)
                )
            
            # Efficiency Metrics Tab
            with tabs[1]:
                col1, col2 = st.columns(2)
                
                with col1:
                    efficiency_score = st.slider(
                        "Overall Efficiency Score (1-10)",
                        1, 10,
                        value=st.session_state.agency_data.get(selected_agency, {}).get('efficiency_score', 5)
                    )
                    
                    budget_utilization = st.slider(
                        "Budget Utilization Efficiency (1-10)",
                        1, 10,
                        value=st.session_state.agency_data.get(selected_agency, {}).get('budget_utilization', 5)
                    )
                
                with col2:
                    service_quality = st.slider(
                        "Service Quality Rating (1-10)",
                        1, 10,
                        value=st.session_state.agency_data.get(selected_agency, {}).get('service_quality', 5)
                    )
                    
                    processing_time = st.slider(
                        "Processing Time Efficiency (1-10)",
                        1, 10,
                        value=st.session_state.agency_data.get(selected_agency, {}).get('processing_time', 5)
                    )
                
                overall_efficiency = calculate_efficiency_metrics(
                    efficiency_score,
                    budget_utilization,
                    service_quality,
                    processing_time
                )
                
                st.metric(
                    "Overall Efficiency Rating",
                    f"{overall_efficiency}/10",
                    delta=round(overall_efficiency - 5, 2)
                )
            
            # Performance History Tab
            with tabs[2]:
                st.area_chart(
                    pd.DataFrame(
                        {
                            'Efficiency': [efficiency_score],
                            'Budget': [budget_utilization],
                            'Quality': [service_quality],
                            'Speed': [processing_time]
                        }
                    )
                )
            
            # Save button
            if st.button("Save Agency Data"):
                st.session_state.agency_data[selected_agency] = {
                    'description': description,
                    'mandate': mandate,
                    'established_date': established_date.strftime('%Y-%m-%d'),
                    'efficiency_score': efficiency_score,
                    'budget_utilization': budget_utilization,
                    'service_quality': service_quality,
                    'processing_time': processing_time,
                    'overall_efficiency': overall_efficiency
                }
                st.success(f"Data saved for {selected_agency}")
            
            # Export functionality
            if st.button("Export Data"):
                st.download_button(
                    label="Download Agency Data",
                    data=json.dumps(st.session_state.agency_data, indent=2),
                    file_name="government_efficiency_data.json",
                    mime="application/json"
                )

if __name__ == "__main__":
    main()
