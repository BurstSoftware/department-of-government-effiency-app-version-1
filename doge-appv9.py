import streamlit as st
import pandas as pd

# Define data for the table
data = {
    "Category": [
        "Process Optimization", 
        "Resource Utilization", 
        "Digital Transformation", 
        "Quality Improvement", 
        "Overall"
    ],
    "Selected Actions": [
        "Standardized workflows, Use of process mapping tools, Regular process reviews and improvements, Elimination of bottlenecks",
        "Optimized labor usage, Efficient use of time, Reduced material waste, Energy efficiency improvements",
        "Automation of tasks, Artificial Intelligence for process improvement, Digital inventory management systems, Use of cloud-based solutions",
        "Elimination of defects, Rigorous quality control measures, Employee training programs for quality assurance, Continuous improvement culture",
        "N/A"
    ],
    "Category Score": [
        "100.00%", 
        "100.00%", 
        "100.00%", 
        "100.00%", 
        "100.00%"
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Streamlit UI
st.title("Efficiency Evaluation Table")

# Display the table
st.write("Here is a summary of your efficiency evaluation:")
st.dataframe(df)

# Option to download the table as CSV
csv = df.to_csv(index=False)
st.download_button(
    label="Download Results as CSV",
    data=csv,
    file_name="efficiency_scores.csv",
    mime="text/csv"
)
