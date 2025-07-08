
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")

st.title("📊 Personal Finance Dashboard")

# --- Inputs ---
gross_salary = 138000
net_income = 89954.4
avg_annual_savings = 51864.78
current_net_worth = 302043.64
annual_expenses = 38089.62
fire_target = 952240.5
years_to_fire = 9

# --- Summary ---
st.header("Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Gross Salary", f"£{gross_salary}")
col2.metric("Net Income", f"£{net_income}")
col3.metric("Savings Rate (Net)", f"{(avg_annual_savings / net_income) * 100:.2f}%")

col4, col5, col6 = st.columns(3)
col4.metric("Start Net Worth", "£302,044")
col5.metric("End Net Worth", "£" + str(round(current_net_worth + avg_annual_savings, 2)))
col6.metric("FIRE Target", f"£{round(fire_target)}")

st.info(f"🕒 Estimated Years to FIRE: **{years_to_fire} years**")

# --- Net Worth Growth Chart ---
st.subheader("📈 Net Worth Projection")
years = list(range(0, years_to_fire + 1))
growth = [current_net_worth * (1.05)**i + avg_annual_savings * ((1.05)**i - 1) / 0.05 for i in years]

fig, ax = plt.subplots()
ax.plot(years, growth, marker='o')
ax.axhline(y=fire_target, color='red', linestyle='--', label='FIRE Target')
ax.set_xlabel("Years")
ax.set_ylabel("Net Worth (£)")
ax.set_title("Projected Net Worth Growth")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# --- Strategy ---
st.subheader("💼 Portfolio Strategy")
st.markdown("""
- Max out **Pension (SIPP or Workplace)**: £60,000/year
- Max out **Stocks & Shares ISA**: £20,000/year
- Use **Global Equity ETFs**: VWRP, IWDG, VEVE
- Use **Gilts/Bonds**: VGOV, IGLS
- Rebalance annually
- Prioritize ISA & Pension for tax-free growth
""")
