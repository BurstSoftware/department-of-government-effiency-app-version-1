import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="Business Efficiency Calculator", layout="wide")

# Title and description
st.title("Business Efficiency Calculator")
st.markdown("""
This application helps you measure and visualize different aspects of business efficiency.
Rate each component based on your current business performance.
""")

# Initialize session state for total weight tracking
if 'total_weight' not in st.session_state:
    st.session_state.total_weight = 0

# Define efficiency categories and their sub-components
efficiency_categories = {
    "Operational Efficiency": {
        "Process Optimization": 0,
        "Waste Reduction": 0,
        "Productivity Levels": 0,
        "Resource Utilization": 0
    },
    "Cost Efficiency": {
        "Expense Management": 0,
        "ROI Performance": 0,
        "Economies of Scale": 0,
        "Overhead Control": 0
    },
    "Time Efficiency": {
        "Production Speed": 0,
        "Bottleneck Management": 0,
        "Turnaround Time": 0,
        "Resource Scheduling": 0
    },
    "Resource Efficiency": {
        "Output per Input": 0,
        "Material Waste Management": 0,
        "Inventory Optimization": 0,
        "HR Utilization": 0
    }
}

# Create columns for different categories
st.header("Efficiency Metrics")
cols = st.columns(len(efficiency_categories))

# Dictionary to store category totals
category_totals = {}

# Create sliders for each category and calculate totals
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
st.header("Overall Business Efficiency")
st.metric("Overall Efficiency Score", f"{total_efficiency:.1f}%")

# Create visualizations
st.header("Efficiency Visualizations")
col1, col2 = st.columns(2)

# Radar Chart for Category Totals
with col1:
    categories = list(category_totals.keys())
    values = list(category_totals.values())
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title="Efficiency Radar Chart"
    )
    st.plotly_chart(fig)

# Bar Chart for Individual Metrics
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

# Recommendations section
st.header("Efficiency Recommendations")
recommendations = []

for category, total in category_totals.items():
    if total < 50:
        recommendations.append(f"⚠️ {category} needs significant improvement (Current: {total}%)")
    elif total < 75:
        recommendations.append(f"📈 {category} has room for optimization (Current: {total}%)")
    else:
        recommendations.append(f"✅ {category} is performing well (Current: {total}%)")

for rec in recommendations:
    st.write(rec)

# Export data option
if st.button("Export Data"):
    export_data = {
        "Category Totals": category_totals,
        "Overall Efficiency": total_efficiency,
        "Detailed Metrics": efficiency_categories
    }
    st.json(export_data)
