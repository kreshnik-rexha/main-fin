
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
st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")
st.title("🔐 Personal Finance Dashboard")

# --- USER INPUTS ---
st.sidebar.header("Customize Your Profile")
gross_salary = st.sidebar.number_input("Gross Annual Salary (£)", value=138000)
net_income = st.sidebar.number_input("Estimated Net Income (£)", value=89954.4)
avg_annual_savings = st.sidebar.number_input("Annual Savings/Investments (£)", value=51864.78)
current_net_worth = st.sidebar.number_input("Current Net Worth (£)", value=302043.64)
annual_expenses = net_income - avg_annual_savings

# --- FIRE TARGET ---
withdrawal_rate = 0.04
fire_target = annual_expenses / withdrawal_rate
years_to_fire = 0
net_worth = current_net_worth
while net_worth < fire_target and years_to_fire < 60:
    net_worth *= 1.05
    net_worth += avg_annual_savings
    years_to_fire += 1

# --- FILE UPLOAD ---
st.sidebar.subheader("Upload Your Financial Data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

# --- METRICS ---
st.header("📊 Financial Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Gross Salary", f"£{gross_salary:,.0f}")
col2.metric("Net Income", f"£{net_income:,.0f}")
col3.metric("Savings Rate (Net)", f"{(avg_annual_savings / net_income) * 100:.2f}%")

col4, col5, col6 = st.columns(3)
col4.metric("Start Net Worth", f"£{current_net_worth:,.0f}")
col5.metric("FIRE Target", f"£{fire_target:,.0f}")
col6.metric("Years to FIRE", years_to_fire)

# --- PLOT: FIRE GROWTH ---
st.subheader("📈 Net Worth Growth to FIRE")
years = list(range(0, years_to_fire + 1))
growth = [current_net_worth * (1.05)**i + avg_annual_savings * ((1.05)**i - 1) / 0.05 for i in years]

fig, ax = plt.subplots()
ax.plot(years, growth, marker='o', label="Projected Net Worth")
ax.axhline(fire_target, color='red', linestyle='--', label='FIRE Target')
ax.set_xlabel("Years")
ax.set_ylabel("Net Worth (£)")
ax.set_title("Net Worth Growth")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# --- OPTIONAL: DATA PREVIEW ---
if uploaded_file:
    st.subheader("📂 Uploaded Financial Data")
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    st.dataframe(df)

# --- STRATEGY ---
st.subheader("💼 Recommended Strategy")
st.markdown("""
- Max out **Pension (SIPP or Workplace)**: £60,000/year
- Max out **Stocks & Shares ISA**: £20,000/year
- Use **Global Equity ETFs**: VWRP, IWDG, VEVE
- Add **Bonds (VGOV, IGLS)** and **REITs** as needed
- Rebalance annually
- Prioritize ISA & SIPP for tax efficiency
""")
