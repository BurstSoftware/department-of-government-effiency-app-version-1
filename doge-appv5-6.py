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
    page_title="Enhanced Government Department Efficiency Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for weights
if 'weights' not in st.session_state:
    st.session_state.weights = {}

def initialize_category_weights(category):
    """Initialize weights for a category if not already in session state"""
    if category not in st.session_state.weights:
        st.session_state.weights[category] = {
            subcategory: 25 for subcategory in efficiency_categories[category].keys()
        }

def adjust_other_weights(category, changed_subcategory, new_weight):
    """Adjusts other weights in the category proportionally when one weight changes"""
    current_weights = st.session_state.weights[category]
    old_weight = current_weights[changed_subcategory]
    other_subcategories = [sub for sub in current_weights.keys() if sub != changed_subcategory]
    
    # Calculate weight difference
    weight_difference = new_weight - old_weight
    
    if weight_difference == 0:
        return
    
    # Calculate total weight of other subcategories
    total_other_weight = sum(current_weights[sub] for sub in other_subcategories)
    
    if total_other_weight == 0:
        # Distribute remaining weight equally
        remaining_weight = (100 - new_weight) / len(other_subcategories)
        for sub in other_subcategories:
            current_weights[sub] = remaining_weight
    else:
        # Adjust other weights proportionally
        for sub in other_subcategories:
            proportion = current_weights[sub] / total_other_weight
            adjustment = weight_difference * proportion
            current_weights[sub] = max(0, current_weights[sub] - adjustment)
    
    # Ensure total is exactly 100
    total = sum(current_weights.values())
    if total != 100:
        difference = 100 - total
        largest_other = max(other_subcategories, key=lambda x: current_weights[x])
        current_weights[largest_other] += difference
    
    # Update the changed subcategory
    current_weights[changed_subcategory] = new_weight

def weight_slider(category, subcategory, key):
    """Creates a weight slider that maintains total weight of 100 within category"""
    initialize_category_weights(category)
    current_weight = st.session_state.weights[category][subcategory]
    
    # Calculate maximum allowed weight
    other_weights = sum(weight for sub, weight in st.session_state.weights[category].items() 
                       if sub != subcategory)
    max_weight = 100 - other_weights + current_weight
    
    new_weight = st.slider(
        f"Weight for {subcategory}",
        0, 100, int(current_weight),
        key=f"weight_{key}",
        help="Adjust weight (other weights will automatically adjust to maintain total of 100)"
    )
    
    if new_weight != current_weight:
        adjust_other_weights(category, subcategory, new_weight)
    
    return new_weight

# [Previous efficiency_categories definition remains the same]

def main():
    st.title("Enhanced Government Department Efficiency Calculator")
    
    tab1, tab2, tab3 = st.tabs(["Efficiency Assessment", "Detailed Metrics", "Visualization"])
    
    selected_metrics = {}
    category_scores = {}
    
    with tab1:
        st.header("Department Information")
        department_name = st.text_input("Department Name")
        
        st.header("Efficiency Categories")
        for category, subcategories in efficiency_categories.items():
            st.subheader(category)
            selected_metrics[category] = {}
            
            # Display current weight distribution
            current_weights = st.session_state.weights.get(category, {})
            if current_weights:
                st.write("Current Weight Distribution:")
                weight_df = pd.DataFrame({
                    'Subcategory': list(current_weights.keys()),
                    'Weight': list(current_weights.values())
                })
                st.dataframe(weight_df)
            
            cols = st.columns(len(subcategories))
            for idx, (subcategory, data) in enumerate(subcategories.items()):
                with cols[idx]:
                    st.write(f"**{subcategory}**")
                    
                    # Use dynamic weight slider
                    weight = weight_slider(category, subcategory, f"{category}_{subcategory}")
                    efficiency_categories[category][subcategory]['weight'] = weight
                    
                    selected = st.multiselect(
                        "Select implemented metrics:",
                        options=list(data['metrics'].keys()),
                        key=f"metrics_{category}_{subcategory}"
                    )
                    selected_metrics[category][subcategory] = selected
            
            # Calculate and display category score
            category_scores[category] = calculate_category_score(
                subcategories,
                selected_metrics[category]
            )
            
            st.metric(f"{category} Score", f"{category_scores[category]:.1f}%")
        
        # Calculate and display overall score
        overall_score = sum(category_scores.values()) / len(category_scores)
        st.header("Overall Efficiency Score")
        st.metric("Overall Score", f"{overall_score:.1f}%")
        
        # Display performance message
        if overall_score >= 80:
            st.success("Excellent efficiency level! Continue maintaining high standards.")
        elif overall_score >= 60:
            st.warning("Good efficiency level with room for improvement.")
        else:
            st.error("Significant improvement needed in efficiency metrics.")

    # [Rest of the visualization code remains the same]

if __name__ == "__main__":
    main()
