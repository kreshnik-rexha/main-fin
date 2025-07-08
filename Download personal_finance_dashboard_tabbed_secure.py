
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- AUTHENTICATION ---
PASSWORD = "secure123"
st.session_state['authenticated'] = st.session_state.get('authenticated', False)

if not st.session_state['authenticated']:
    pwd = st.text_input("Enter password to access dashboard:", type="password")
    if pwd == PASSWORD:
        st.session_state['authenticated'] = True
        st.success("Authenticated. Please reload the page.")
            st.stop()
    else:
            st.stop()

# --- PAGE SETUP ---
st.set_page_config(page_title="Finance Dashboard", layout="wide")

st.title("📊 Personal Finance Dashboard")

# --- SIDEBAR ---
st.sidebar.header("Customize Inputs")
gross_salary = st.sidebar.number_input("Gross Annual Salary (£)", value=138000)
net_income = st.sidebar.number_input("Estimated Net Income (£)", value=89954.4)
avg_annual_savings = st.sidebar.number_input("Annual Savings/Investments (£)", value=51864.78)
current_net_worth = st.sidebar.number_input("Current Net Worth (£)", value=302043.64)
annual_expenses = net_income - avg_annual_savings
uploaded_file = st.sidebar.file_uploader("Upload your finance file (.csv or .xlsx)", type=["csv", "xlsx"])

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🔥 FIRE Tracker", "📊 Asset Analysis", "📂 Upload & Explore"])

# --- TAB 1: Overview ---
with tab1:
    st.header("📈 Financial Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Gross Salary", f"£{gross_salary:,.0f}")
    col2.metric("Net Income", f"£{net_income:,.0f}")
    col3.metric("Savings Rate (Net)", f"{(avg_annual_savings / net_income) * 100:.2f}%")

    col4, col5, col6 = st.columns(3)
    col4.metric("Current Net Worth", f"£{current_net_worth:,.0f}")
    col5.metric("Annual Expenses", f"£{annual_expenses:,.0f}")
    col6.metric("Savings (Annual)", f"£{avg_annual_savings:,.0f}")

# --- TAB 2: FIRE Tracker ---
with tab2:
    st.header("🔥 FIRE Tracker")
    withdrawal_rate = 0.04
    fire_target = annual_expenses / withdrawal_rate
    years_to_fire = 0
    net_worth = current_net_worth
    while net_worth < fire_target and years_to_fire < 60:
        net_worth *= 1.05
        net_worth += avg_annual_savings
        years_to_fire += 1

    st.success(f"Estimated Years to FIRE: **{years_to_fire} years**")
    years = list(range(0, years_to_fire + 1))
    growth = [current_net_worth * (1.05)**i + avg_annual_savings * ((1.05)**i - 1) / 0.05 for i in years]

    fig, ax = plt.subplots()
    ax.plot(years, growth, marker='o', label="Net Worth")
    ax.axhline(fire_target, color='red', linestyle='--', label='FIRE Target')
    ax.set_xlabel("Years")
    ax.set_ylabel("Net Worth (£)")
    ax.set_title("Net Worth Growth to FIRE")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

# --- TAB 3: Asset Analysis ---
with tab3:
    st.header("📊 Asset Allocation Strategy")
    st.markdown("""
    - Use your **SIPP or Workplace Pension** to defer tax and invest long-term
    - Max out your **ISA** for tax-free growth
    - Use low-cost **equity ETFs**: `VWRP`, `VEVE`, `IWDG`
    - Add **bonds (VGOV, IGLS)** and **REITs (IWDP)** for diversification
    - Rebalance yearly within tax-sheltered accounts
    """)

# --- TAB 4: Upload & Explore ---
with tab4:
    st.header("📂 Upload & Explore Financial Data")
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.success("File uploaded successfully!")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error reading file: {e}")
    else:
        st.info("Upload a `.csv` or `.xlsx` file in the sidebar to begin.")
