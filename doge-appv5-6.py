import streamlit as st
import pandas as pd

# Define efficiency categories with corresponding actions and their weights
efficiency_categories = {
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

# Function to calculate category score
def calculate_category_score(selected_actions, category_weights):
    total_weight = sum(category_weights.values())
    selected_weight = sum(category_weights[action] for action in selected_actions)
    return (selected_weight / total_weight) * 100  # Score as percentage

# Function to generate and display the overall efficiency score and actions
def main():
    st.title("Efficiency Evaluation")
    st.write("Evaluate the efficiency of your department or processes based on the following categories.")

    # Store individual category scores
    category_scores = []
    selected_actions_all_categories = []

    # Loop through each category and collect user input
    for category, actions in efficiency_categories.items():
        st.subheader(f"{category}")
        selected_actions = st.multiselect(f"Select actions under {category}:", options=list(actions.keys()))
        
        # Store selected actions for download later
        selected_actions_all_categories.append({"Category": category, "Selected Actions": ", ".join(selected_actions)})
        
        # Calculate and display category score
        category_score = calculate_category_score(selected_actions, actions)
        category_scores.append(category_score)
        st.write(f"Category Score for {category}: {category_score:.2f}%")
    
    # Calculate overall efficiency score
    overall_score = sum(category_scores) / len(category_scores)
    st.subheader("Overall Efficiency Score")
    st.write(f"Your overall efficiency score is: {overall_score:.2f}%")

    # Provide insights based on the overall score
    if overall_score > 80:
        st.success("Your department is highly efficient. Keep up the great work!")
    elif overall_score > 50:
        st.warning("Your department is moderately efficient. There are opportunities for improvement.")
    else:
        st.error("Your department is underperforming. Focus on improving key areas for better efficiency.")
    
    # Create a DataFrame for download
    df = pd.DataFrame(selected_actions_all_categories)
    df = df.append({"Category": "Overall", "Selected Actions": "N/A", "Category Score": f"{overall_score:.2f}%"}, ignore_index=True)

    # Button for downloading CSV
    st.subheader("Download your results")
    st.download_button(
        label="Download Results as CSV",
        data=df.to_csv(index=False),
        file_name="efficiency_results.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()
