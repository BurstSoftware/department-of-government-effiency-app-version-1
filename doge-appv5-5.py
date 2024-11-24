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

# Initialize session state
if 'total_weight' not in st.session_state:
    st.session_state.total_weight = 0
if 'selected_agency' not in st.session_state:
    st.session_state.selected_agency = None

# Define efficiency categories with detailed metrics and default weights
efficiency_categories = {
    "Operational Efficiency": {
        "Process Optimization": {
            "weight": 25,
            "metrics": {
                "Standardized workflows": 10,
                "Process mapping implementation": 8,
                "Regular process reviews": 6,
                "Bottleneck elimination": 9
            }
        },
        "Resource Utilization": {
            "weight": 25,
            "metrics": {
                "Labor optimization": 9,
                "Time management": 8,
                "Resource waste reduction": 7,
                "Energy efficiency": 6
            }
        },
        "Service Delivery Speed": {
            "weight": 25,
            "metrics": {
                "Response time": 10,
                "Service completion rate": 8,
                "Queue management": 7,
                "Service automation": 8
            }
        },
        "Digital Transformation": {
            "weight": 25,
            "metrics": {
                "Process automation": 10,
                "Digital systems adoption": 9,
                "Cloud solution usage": 8,
                "AI implementation": 7
            }
        }
    },
    "Fiscal Efficiency": {
        "Budget Management": {
            "weight": 25,
            "metrics": {
                "Budget utilization": 10,
                "Cost forecasting": 8,
                "Budget monitoring": 7,
                "Financial planning": 8
            }
        },
        "Cost Control": {
            "weight": 25,
            "metrics": {
                "Expense reduction": 9,
                "Cost monitoring": 8,
                "Vendor management": 7,
                "Resource optimization": 8
            }
        },
        "Resource Allocation": {
            "weight": 25,
            "metrics": {
                "Fund distribution": 9,
                "Resource prioritization": 8,
                "Asset management": 7,
                "Investment planning": 8
            }
        },
        "Financial Transparency": {
            "weight": 25,
            "metrics": {
                "Financial reporting": 10,
                "Audit compliance": 9,
                "Stakeholder communication": 7,
                "Data accessibility": 8
            }
        }
    },
    "Administrative Efficiency": {
        "Paperwork Processing": {
            "weight": 25,
            "metrics": {
                "Document digitization": 10,
                "Workflow automation": 9,
                "Processing speed": 8,
                "Error reduction": 7
            }
        },
        "Response Time": {
            "weight": 25,
            "metrics": {
                "Query handling": 9,
                "Service delivery": 8,
                "Communication speed": 7,
                "Issue resolution": 8
            }
        },
        "Staff Productivity": {
            "weight": 25,
            "metrics": {
                "Task completion": 9,
                "Work quality": 8,
                "Time management": 7,
                "Goal achievement": 8
            }
        },
        "Regulatory Compliance": {
            "weight": 25,
            "metrics": {
                "Policy adherence": 10,
                "Documentation": 8,
                "Audit readiness": 7,
                "Compliance monitoring": 8
            }
        }
    },
    "Public Service Efficiency": {
        "Citizen Satisfaction": {
            "weight": 25,
            "metrics": {
                "Service quality": 10,
                "Feedback management": 8,
                "Complaint resolution": 7,
                "User experience": 8
            }
        },
        "Service Accessibility": {
            "weight": 25,
            "metrics": {
                "Digital access": 9,
                "Physical access": 8,
                "Information availability": 7,
                "Support services": 8
            }
        },
        "Communication Effectiveness": {
            "weight": 25,
            "metrics": {
                "Clear messaging": 9,
                "Channel effectiveness": 8,
                "Response quality": 7,
                "Public engagement": 8
            }
        },
        "Public Engagement": {
            "weight": 25,
            "metrics": {
                "Community involvement": 9,
                "Feedback collection": 8,
                "Public consultation": 7,
                "Stakeholder engagement": 8
            }
        }
    }
}

def calculate_metric_score(selected_metrics, metrics_dict):
    total_weight = sum(metrics_dict.values())
    selected_weight = sum(metrics_dict[metric] for metric in selected_metrics)
    return (selected_weight / total_weight) * 100

def calculate_category_score(category_data, selected_metrics):
    scores = []
    weights = []
    
    for subcategory, data in category_data.items():
        if subcategory in selected_metrics:
            score = calculate_metric_score(
                selected_metrics[subcategory],
                data['metrics']
            )
            weight = data['weight']
            scores.append(score)
            weights.append(weight)
    
    if not scores:
        return 0
    
    weighted_score = sum(s * w for s, w in zip(scores, weights)) / sum(weights)
    return weighted_score

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
            
            cols = st.columns(len(subcategories))
            for idx, (subcategory, data) in enumerate(subcategories.items()):
                with cols[idx]:
                    st.write(f"**{subcategory}**")
                    weight = st.slider(
                        f"Weight for {subcategory}",
                        0, 100, data['weight'],
                        key=f"weight_{category}_{subcategory}"
                    )
                    efficiency_categories[category][subcategory]['weight'] = weight
                    
                    selected = st.multiselect(
                        "Select implemented metrics:",
                        options=list(data['metrics'].keys()),
                        key=f"metrics_{category}_{subcategory}"
                    )
                    selected_metrics[category][subcategory] = selected
            
            category_scores[category] = calculate_category_score(
                subcategories,
                selected_metrics[category]
            )
            
            st.metric(f"{category} Score", f"{category_scores[category]:.1f}%")
        
        overall_score = sum(category_scores.values()) / len(category_scores)
        st.header("Overall Efficiency Score")
        st.metric("Overall Score", f"{overall_score:.1f}%")
        
        if overall_score >= 80:
            st.success("Excellent efficiency level! Continue maintaining high standards.")
        elif overall_score >= 60:
            st.warning("Good efficiency level with room for improvement.")
        else:
            st.error("Significant improvement needed in efficiency metrics.")
    
    with tab2:
        st.header("Detailed Metric Analysis")
        for category, score in category_scores.items():
            with st.expander(f"{category} - {score:.1f}%"):
                for subcategory, data in efficiency_categories[category].items():
                    st.subheader(subcategory)
                    selected = selected_metrics[category].get(subcategory, [])
                    metrics_df = pd.DataFrame({
                        'Metric': data['metrics'].keys(),
                        'Weight': data['metrics'].values(),
                        'Implemented': ['Yes' if m in selected else 'No' for m in data['metrics'].keys()]
                    })
                    st.dataframe(metrics_df)
    
    with tab3:
        st.header("Efficiency Visualizations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Radar Chart
            categories = list(category_scores.keys())
            values = list(category_scores.values())
            
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
        
        with col2:
            # Bar Chart
            df_scores = pd.DataFrame({
                'Category': categories,
                'Score': values
            })
            
            fig = px.bar(
                df_scores,
                x='Category',
                y='Score',
                title="Category Scores Comparison"
            )
            
            fig.update_layout(yaxis_range=[0, 100])
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()
