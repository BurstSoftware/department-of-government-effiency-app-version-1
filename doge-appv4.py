import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime
import uuid

# Configuration and Page Setup
st.set_page_config(
    page_title="Business Efficiency Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
def init_session_state():
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'current_assessment_id' not in st.session_state:
        st.session_state.current_assessment_id = str(uuid.uuid4())

init_session_state()

# Data Models
EFFICIENCY_CATEGORIES = {
    "Operational Efficiency": {
        "Process Optimization": {
            "weight": 25,
            "description": "Measure of workflow and process effectiveness"
        },
        "Waste Reduction": {
            "weight": 25,
            "description": "Effectiveness in minimizing resource waste"
        },
        "Productivity Levels": {
            "weight": 25,
            "description": "Output per unit of input"
        },
        "Resource Utilization": {
            "weight": 25,
            "description": "Efficiency of resource usage"
        }
    },
    "Cost Efficiency": {
        "Expense Management": {
            "weight": 25,
            "description": "Control over operational expenses"
        },
        "ROI Performance": {
            "weight": 25,
            "description": "Return on investment metrics"
        },
        "Economies of Scale": {
            "weight": 25,
            "description": "Cost advantages from scale"
        },
        "Overhead Control": {
            "weight": 25,
            "description": "Management of indirect costs"
        }
    },
    "Time Efficiency": {
        "Production Speed": {
            "weight": 25,
            "description": "Speed of production processes"
        },
        "Bottleneck Management": {
            "weight": 25,
            "description": "Effectiveness in handling delays"
        },
        "Turnaround Time": {
            "weight": 25,
            "description": "Time from start to completion"
        },
        "Resource Scheduling": {
            "weight": 25,
            "description": "Efficiency of resource allocation"
        }
    },
    "Resource Efficiency": {
        "Output per Input": {
            "weight": 25,
            "description": "Resource utilization effectiveness"
        },
        "Material Waste Management": {
            "weight": 25,
            "description": "Control over material waste"
        },
        "Inventory Optimization": {
            "weight": 25,
            "description": "Inventory management efficiency"
        },
        "HR Utilization": {
            "weight": 25,
            "description": "Human resource effectiveness"
        }
    }
}

# Utility Functions
def calculate_category_score(metrics):
    return sum(metrics.values())

def calculate_overall_efficiency(category_scores):
    return sum(category_scores.values()) / len(category_scores)

def generate_recommendations(category_scores):
    recommendations = []
    priority_levels = {
        (0, 50): ("Critical", "🔴"),
        (50, 75): ("Moderate", "🟡"),
        (75, 101): ("Good", "🟢")
    }
    
    for category, score in category_scores.items():
        for (lower, upper), (priority, icon) in priority_levels.items():
            if lower <= score < upper:
                recommendations.append({
                    "category": category,
                    "score": score,
                    "priority": priority,
                    "icon": icon,
                    "recommendation": f"{icon} {category}: {priority} priority - Score: {score:.1f}%"
                })
                break
    
    return sorted(recommendations, key=lambda x: x["score"])

# Main Application
def main():
    st.title("🎯 Business Efficiency Analytics Dashboard")
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header("Assessment Controls")
        company_name = st.text_input("Company Name", "My Company")
        assessment_date = st.date_input("Assessment Date", datetime.now())
        st.markdown("---")
        st.markdown("### Instructions")
        st.markdown("""
        1. Rate each metric from 0-25
        2. Review the visualizations
        3. Export your results
        4. Track progress over time
        """)

    # Main Content
    tab1, tab2, tab3 = st.tabs(["Assessment", "Visualizations", "History"])

    # Tab 1: Assessment
    with tab1:
        category_scores = {}
        metric_scores = {}
        
        for category, metrics in EFFICIENCY_CATEGORIES.items():
            st.subheader(f"📊 {category}")
            cols = st.columns(2)
            
            metric_scores[category] = {}
            for idx, (metric, details) in enumerate(metrics.items()):
                with cols[idx % 2]:
                    st.markdown(f"**{metric}**")
                    st.caption(details["description"])
                    value = st.slider(
                        f"{metric}",
                        0, 25, 0,
                        help=f"Rate {metric} (0-25)",
                        key=f"{category}_{metric}"
                    )
                    metric_scores[category][metric] = value
            
            category_scores[category] = calculate_category_score(metric_scores[category])
            st.progress(category_scores[category]/100)
            st.markdown("---")

        overall_efficiency = calculate_overall_efficiency(category_scores)

    # Tab 2: Visualizations
    with tab2:
        col1, col2 = st.columns(2)
        
        # Radar Chart
        with col1:
            categories = list(category_scores.keys())
            values = list(category_scores.values())
            
            fig_radar = go.Figure(data=go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Current Assessment'
            ))
            
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=True,
                title="Efficiency Radar Chart"
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        # Detailed Metrics Bar Chart
        with col2:
            metrics_data = []
            for category, metrics in metric_scores.items():
                for metric, value in metrics.items():
                    metrics_data.append({
                        "Category": category,
                        "Metric": metric,
                        "Value": value
                    })
            
            df_metrics = pd.DataFrame(metrics_data)
            fig_bar = px.bar(
                df_metrics,
                x="Value",
                y="Metric",
                color="Category",
                title="Detailed Metrics Breakdown",
                orientation='h'
            )
            fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_bar, use_container_width=True)

        # Recommendations
        st.subheader("📋 Recommendations")
        recommendations = generate_recommendations(category_scores)
        cols = st.columns(3)
        for idx, rec in enumerate(recommendations):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>{rec['icon']} {rec['category']}</h4>
                    <p>Priority: {rec['priority']}</p>
                    <p>Score: {rec['score']:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)

    # Tab 3: History
    with tab3:
        if st.button("Save Current Assessment"):
            assessment_data = {
                "id": st.session_state.current_assessment_id,
                "company_name": company_name,
                "date": assessment_date.strftime("%Y-%m-%d"),
                "overall_efficiency": overall_efficiency,
                "category_scores": category_scores,
                "metric_scores": metric_scores
            }
            st.session_state.history.append(assessment_data)
            st.session_state.current_assessment_id = str(uuid.uuid4())
            st.success("Assessment saved!")

        if st.session_state.history:
            history_df = pd.DataFrame([
                {
                    "Date": h["date"],
                    "Company": h["company_name"],
                    "Overall Efficiency": h["overall_efficiency"],
                    **h["category_scores"]
                }
                for h in st.session_state.history
            ])
            
            st.line_chart(history_df.set_index("Date")["Overall Efficiency"])
            st.dataframe(history_df)

    # Export Options
    st.sidebar.markdown("---")
    if st.sidebar.button("Export Assessment"):
        export_data = {
            "assessment_id": st.session_state.current_assessment_id,
            "company_name": company_name,
            "date": assessment_date.strftime("%Y-%m-%d"),
            "overall_efficiency": overall_efficiency,
            "category_scores": category_scores,
            "metric_scores": metric_scores,
            "recommendations": recommendations
        }
        
        st.sidebar.download_button(
            label="📥 Download JSON",
            file_name=f"efficiency_assessment_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            data=json.dumps(export_data, indent=2)
        )

if __name__ == "__main__":
    main()
