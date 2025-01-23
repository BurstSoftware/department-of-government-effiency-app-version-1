import streamlit as st

def calculate_efficiency(output, input_):
    """Calculate efficiency as a percentage."""
    return (output / input_) * 100

def main():
    st.title("Efficiency from First Principles")

    # Introduction
    st.write("Efficiency measures how useful your system or machine is, calculated as: \( \eta = \frac{\text{Output}}{\text{Input}} \times 100\% \)")

    st.subheader("General Efficiency Calculator")
    output = st.number_input("Enter Output Value:", min_value=0.0, step=1.0)
    input_ = st.number_input("Enter Input Value:", min_value=0.0, step=1.0)

    if input_ > 0:
        efficiency = calculate_efficiency(output, input_)
        st.write(f"Efficiency: {efficiency:.2f}%")
    else:
        st.warning("Input must be greater than zero to calculate efficiency.")

    st.subheader("Tax-Based Efficiency Calculations")

    # Efficiency using taxes and working Americans
    st.write("1. Efficiency based on taxes per 161 million working Americans:")
    taxes = st.number_input("Enter Total Taxes Collected (in dollars):", min_value=0.0, step=1.0)
    working_americans = 161_000_000  # fixed value

    if taxes > 0:
        tax_efficiency = calculate_efficiency(taxes, working_americans)
        st.write(f"Tax Efficiency: {tax_efficiency:.2f}%")
    else:
        st.warning("Taxes must be greater than zero to calculate tax efficiency.")

    # Efficiency using taxes and total Americans
    st.write("2. Efficiency based on total tax dollars per 341 million Americans:")
    total_americans = 341_000_000  # fixed value

    if taxes > 0:
        tax_per_american = taxes / total_americans
        st.write(f"Tax per American: ${tax_per_american:.2f}")
    else:
        st.warning("Taxes must be greater than zero to calculate tax per American.")

    # Inefficient tax dollars per American
    st.write("3. Inefficient tax dollars per 341 million Americans:")
    inefficient_taxes = st.number_input("Enter Total Inefficient Tax Dollars (in dollars):", min_value=0.0, step=1.0)

    if inefficient_taxes > 0:
        inefficient_tax_per_american = inefficient_taxes / total_americans
        st.write(f"Inefficient Tax per American: ${inefficient_tax_per_american:.2f}")
    else:
        st.warning("Inefficient taxes must be greater than zero to calculate inefficient tax per American.")

    # Conditional statement regarding tax dollars per American
    st.subheader("Analysis")
    if taxes > 0 and tax_per_american > 10000:
        st.write("The tax burden per American is high, indicating inefficiency.")
    elif taxes > 0:
        st.write("The tax burden per American is reasonable, indicating potential efficiency.")

if __name__ == "__main__":
    main()
