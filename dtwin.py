#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

# --- SETTING PAGE CONFIG ---
st.set_page_config(page_title="Digital Twin - Automotive Supply Chain", layout="wide")

# --- SIMULATING SUPPLY CHAIN DATA ---
np.random.seed(42)
dates = pd.date_range(start="2024-01-01", periods=30, freq="D")

data = {
    "Date": dates,
    "Inventory Level": np.random.randint(500, 1000, size=30),
    "Supplier Reliability (%)": np.random.uniform(75, 99, size=30),
    "Shipment Delays (Days)": np.random.randint(0, 5, size=30),
    "Demand Forecast": np.random.randint(400, 1200, size=30),
}

df = pd.DataFrame(data)

# --- MACHINE LEARNING MODEL FOR DEMAND PREDICTION ---
X = np.array(range(30)).reshape(-1, 1)
y = df["Demand Forecast"].values

model = LinearRegression()
model.fit(X, y)
future_days = np.array(range(30, 40)).reshape(-1, 1)
predicted_demand = model.predict(future_days)

# --- STREAMLIT UI ---
st.title("🚗 Digital Twin: Automotive Supply Chain Dashboard")
st.markdown("### Real-time supply chain monitoring & AI-powered predictions")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📦 Inventory Level", f"{df['Inventory Level'].iloc[-1]} units")

with col2:
    st.metric("✅ Supplier Reliability", f"{df['Supplier Reliability (%)'].iloc[-1]:.2f}%")

with col3:
    st.metric("🚚 Avg. Shipment Delay", f"{df['Shipment Delays (Days)'].mean():.1f} days")

# --- DATA VISUALIZATION ---
st.subheader("📊 Inventory Levels Over Time")
fig_inventory = px.line(df, x="Date", y="Inventory Level", title="Inventory Trend")
st.plotly_chart(fig_inventory)

st.subheader("📈 Demand Forecasting (Next 10 Days)")
future_dates = [datetime(2024, 2, 1) + timedelta(days=i) for i in range(10)]
df_future = pd.DataFrame({"Date": future_dates, "Predicted Demand": predicted_demand})
fig_demand = px.line(df_future, x="Date", y="Predicted Demand", title="Predicted Demand Trend", markers=True)
st.plotly_chart(fig_demand)

# --- USER INTERACTION: SCENARIO SIMULATION ---
st.subheader("⚙️ Scenario Testing: Impact of Supply Chain Disruptions")

supplier_drop = st.slider("📉 Supplier Reliability Drop (%)", 0, 50, 10)
delay_increase = st.slider("⏳ Shipment Delay Increase (Days)", 0, 10, 2)

new_reliability = df["Supplier Reliability (%)"].iloc[-1] - supplier_drop
new_delay = df["Shipment Delays (Days)"].mean() + delay_increase

st.write(f"📢 **Updated Supplier Reliability:** {max(new_reliability, 0):.2f}%")
st.write(f"🚛 **Updated Avg. Shipment Delay:** {new_delay:.1f} days")

# --- FOOTER ---
st.markdown("**Built by Team Eureka, IIM Mumbai 🚀**")

