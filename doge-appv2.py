import streamlit as st
import pandas as pd

def calculate_efficiency_score(employees, budget, utilization, oversight, effectiveness_score):
    """Calculate department efficiency score based on key metrics."""
    score = (
        (utilization * 0.3) +          # Budget utilization
        ((100 - oversight) * 0.2) +    # Less oversight means more efficiency
        (min(2000 / employees, 100) * 0.2) +  # Staff efficiency
        (effectiveness_score * 0.3)     # Overall effectiveness impact
    )
    return min(score, 100)

def calculate_effectiveness_score(metrics):
    """Calculate effectiveness score from 1-5 ratings."""
    return sum(metrics) / len(metrics) * 20

def main():
    st.title("U.S. Department Efficiency Calculator")
    
    # Basic Department Information
    department_name = st.text_input("Department Name", "Department of Transportation")
    employees = st.number_input("Number of Full-Time Employees (FTE)", 
                              min_value=1, value=100)
    budget = st.number_input("Annual Budget (in Million USD)", 
                           min_value=0.1, value=50.0)
    
    # Performance Metrics
    st.subheader("Performance Metrics")
    utilization = st.slider("Budget Utilization (%)", 0, 100, 75,
                          help="Percentage of allocated budget effectively used")
    oversight = st.slider("Administrative Overhead (%)", 0, 100, 30,
                         help="Percentage of resources spent on administrative tasks")
    
    # Effectiveness Ratings
    st.subheader("Department Effectiveness Ratings (1-5)")
    col1, col2 = st.columns(2)
    
    with col1:
        service_quality = st.select_slider(
            "Service Quality",
            options=[1, 2, 3, 4, 5],
            value=3,
            format_func=lambda x: ["Very Poor", "Poor", "Average", "Good", "Excellent"][x-1]
        )
        response_time = st.select_slider(
            "Response Time",
            options=[1, 2, 3, 4, 5],
            value=3,
            format_func=lambda x: ["Very Poor", "Poor", "Average", "Good", "Excellent"][x-1]
        )
    
    with col2:
        public_satisfaction = st.select_slider(
            "Public Satisfaction",
            options=[1, 2, 3, 4, 5],
            value=3,
            format_func=lambda x: ["Very Poor", "Poor", "Average", "Good", "Excellent"][x-1]
        )
        cost_effectiveness = st.select_slider(
            "Cost Effectiveness",
            options=[1, 2, 3, 4, 5],
            value=3,
            format_func=lambda x: ["Very Poor", "Poor", "Average", "Good", "Excellent"][x-1]
        )
    
    # Calculate Scores
    effectiveness_metrics = [service_quality, response_time, 
                           public_satisfaction, cost_effectiveness]
    effectiveness_score = calculate_effectiveness_score(effectiveness_metrics)
    efficiency_score = calculate_efficiency_score(employees, budget, utilization, 
                                                oversight, effectiveness_score)
    
    # Display Results
    st.header("Results")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Effectiveness Score", f"{effectiveness_score:.1f}%")
    with col2:
        st.metric("Efficiency Score", f"{efficiency_score:.1f}%")
    
    # Export Data
    if st.button("Download Report"):
        data = {
            "Department": department_name,
            "Employees": employees,
            "Budget_Million_USD": budget,
            "Budget_Utilization": utilization,
            "Administrative_Overhead": oversight,
            "Effectiveness_Score": effectiveness_score,
            "Efficiency_Score": efficiency_score
        }
        df = pd.DataFrame([data])
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download CSV Report",
            csv,
            "department_efficiency_report.csv",
            "text/csv"
        )

if __name__ == "__main__":
    main()
