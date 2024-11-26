import streamlit as st
import pandas as pd

# Title of the app
st.title("Business Efficiency Tracker")

# Sidebar for input
st.sidebar.header("Input Data")
input_type = st.sidebar.selectbox(
    "Select the Business Area", 
    ["Manufacturing", "Sales", "Customer Service"]
)

if input_type == "Manufacturing":
    st.sidebar.subheader("Input Details")
    labor_hours = st.sidebar.number_input("Labor Hours", min_value=0, value=1000)
    raw_materials = st.sidebar.number_input("Raw Materials (Units)", min_value=0, value=600)
    energy_consumption = st.sidebar.number_input("Energy Consumption (kWh)", min_value=0, value=500)

    st.sidebar.subheader("Output Details")
    products_produced = st.sidebar.number_input("Products Produced", min_value=0, value=500)

elif input_type == "Sales":
    st.sidebar.subheader("Input Details")
    sales_team_hours = st.sidebar.number_input("Sales Team Hours", min_value=0, value=200)
    marketing_spend = st.sidebar.number_input("Marketing Budget ($)", min_value=0, value=10000)
    leads_generated = st.sidebar.number_input("Leads Generated", min_value=0, value=100)

    st.sidebar.subheader("Output Details")
    sales_closed = st.sidebar.number_input("Sales Closed", min_value=0, value=50)
    revenue_generated = st.sidebar.number_input("Revenue Generated ($)", min_value=0, value=100000)

elif input_type == "Customer Service":
    st.sidebar.subheader("Input Details")
    agent_hours = st.sidebar.number_input("Agent Hours", min_value=0, value=1000)
    training_resources = st.sidebar.number_input("Training Resources ($)", min_value=0, value=500)

    st.sidebar.subheader("Output Details")
    inquiries_resolved = st.sidebar.number_input("Inquiries Resolved", min_value=0, value=200)
    satisfaction_rate = st.sidebar.number_input("Customer Satisfaction (%)", min_value=0, value=80)

# Calculate Efficiency
def calculate_efficiency(output, input_value):
    return (output / input_value) * 100 if input_value != 0 else 0

# Creating a dataframe to display the results
if input_type == "Manufacturing":
    efficiency_labor = calculate_efficiency(products_produced, labor_hours)
    efficiency_materials = calculate_efficiency(products_produced, raw_materials)
    efficiency_energy = calculate_efficiency(products_produced, energy_consumption)

    data = {
        "Input Type": ["Labor Hours", "Raw Materials", "Energy Consumption"],
        "Input Value": [labor_hours, raw_materials, energy_consumption],
        "Output": [products_produced, products_produced, products_produced],
        "Efficiency (%)": [efficiency_labor, efficiency_materials, efficiency_energy]
    }

elif input_type == "Sales":
    efficiency_labor = calculate_efficiency(sales_closed, sales_team_hours)
    efficiency_marketing = calculate_efficiency(revenue_generated, marketing_spend)

    data = {
        "Input Type": ["Sales Team Hours", "Marketing Spend ($)"],
        "Input Value": [sales_team_hours, marketing_spend],
        "Output": [sales_closed, revenue_generated],
        "Efficiency (%)": [efficiency_labor, efficiency_marketing]
    }

elif input_type == "Customer Service":
    efficiency_labor = calculate_efficiency(inquiries_resolved, agent_hours)
    efficiency_training = calculate_efficiency(satisfaction_rate, training_resources)

    data = {
        "Input Type": ["Agent Hours", "Training Resources ($)"],
        "Input Value": [agent_hours, training_resources],
        "Output": [inquiries_resolved, satisfaction_rate],
        "Efficiency (%)": [efficiency_labor, efficiency_training]
    }

# Display the results
df = pd.DataFrame(data)
st.write(f"### Efficiency Calculation for {input_type}")
st.write(df)

# Plotting a bar chart for efficiency
st.bar_chart(df.set_index("Input Type")["Efficiency (%)"])
