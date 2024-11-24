import streamlit as st
import pandas as pd

# Define efficiency categories and actions with weights
categories = {
    "Process Optimization": {
        "Standardized workflows": 10,
        "Use of process mapping tools": 8,
        "Regular process reviews and improvements": 6,
        "Elimination of bottlenecks": 9
    },
    "Resource Utilization": {
        "Optimized labor usage": 9,
        "Efficient use of time": 8,
        "Reduced material waste": 7,
        "Energy efficiency improvements": 6
    },
    "Digital Transformation": {
        "Automation of tasks": 10,
        "Digital inventory management systems": 9,
        "Use of cloud-based solutions": 8,
        "Artificial Intelligence for process improvement": 7
    },
    "Quality Improvement": {
        "Elimination of defects": 10,
        "Rigorous quality control measures": 9,
        "Employee training programs for quality assurance": 8,
        "Continuous improvement culture": 7
    }
}

# Function to calculate category score based on selected items
def calculate_category_score(selected_actions, category):
    total_weight = sum(category.values())
    selected_weight = sum(category[action] for action in selected_actions)
    return (selected_weight / total_weight) * 100  # Return score as percentage

# Function to calculate overall efficiency
def calculate_overall_efficiency(scores):
    return sum(scores) / len(scores)  # Average of all category scores

# Streamlit App UI
st.title("Efficiency Calculator Application")
st.write("Evaluate the efficiency of your department or processes based on the following categories.")

category_scores = []
selected_actions_dict = []

# Category selection and score calculation
for category, actions in categories.items():
    st.subheader(f"{category}")
    selected_actions = st.multiselect(f"Select actions under {category}:", options=list(actions.keys()))
    category_score = calculate_category_score(selected_actions, actions)
    st.write(f"Category Score: {category_score:.2f}%")
    category_scores.append(category_score)
    selected_actions_dict.append({
        "Category": category,
        "Selected Actions": ', '.join(selected_actions),
        "Category Score": f"{category_score:.2f}%"
    })

# Calculate overall efficiency score
overall_score = calculate_overall_efficiency(category_scores)
st.subheader(f"Overall Efficiency Score")
st.write(f"Your overall efficiency score is: {overall_score:.2f}%")

# Provide insights based on the score
if overall_score > 80:
    st.success("Your department is highly efficient. Keep up the great work!")
elif overall_score > 50:
    st.warning("Your department is moderately efficient. There are opportunities for improvement.")
else:
    st.error("Your department is underperforming. Focus on improving key areas for better efficiency.")

# Create a DataFrame to store the results
df = pd.DataFrame(selected_actions_dict)

# Add a row for the overall score at the end using pd.concat
overall_row = pd.DataFrame([{
    "Category": "Overall", 
    "Selected Actions": "N/A", 
    "Category Score": f"{overall_score:.2f}%"
}])

# Concatenate the overall row to the DataFrame
df = pd.concat([df, overall_row], ignore_index=True)

# Provide the download button for the CSV
csv = df.to_csv(index=False)
st.download_button(
    label="Download Results as CSV",
    data=csv,
    file_name="efficiency_scores.csv",
    mime="text/csv"
)
