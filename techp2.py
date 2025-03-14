#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import folium
from streamlit_folium import st_folium
import time
import smtplib
from email.mime.text import MIMEText
import io

# Set page configuration
st.set_page_config(page_title="Quick Commerce Dashboard", layout="wide")

# Theme toggle in sidebar
st.sidebar.header("Theme Settings")
theme = st.sidebar.radio("Choose Theme", ["Light", "Dark"])
if theme == "Dark":
    st.markdown(
        """
        <style>
        body {background-color: #1a1a1a; color: #ffffff;}
        </style>
        """,
        unsafe_allow_html=True
    )

# Title of the app
st.title("🏬 Quick Commerce Dashboard")

# Generate synthetic data
np.random.seed(42)
num_orders = 300
num_hubs = 15
num_drivers = 15

# Simulate hub locations (latitude, longitude) for map visualization
hub_locations = {
    hub_id: (np.random.uniform(12.9, 13.1), np.random.uniform(77.5, 77.7))
    for hub_id in range(1, num_hubs + 1)
}

# Create a DataFrame for orders
orders_data = {
    "Order_ID": range(1, num_orders + 1),
    "Hub_ID": np.random.choice(range(1, num_hubs + 1), num_orders),
    "Driver_ID": np.random.choice(range(1, num_drivers + 1), num_orders),
    "Order_Value": np.random.uniform(10, 100, num_orders).round(2),
    "Delivery_Time_Minutes": np.random.randint(10, 60, num_orders),
    "Status": np.random.choice(["Delivered", "In Transit", "Pending"], num_orders),
    "Customer_Lat": np.random.uniform(12.9, 13.1, num_orders),
    "Customer_Lon": np.random.uniform(77.5, 77.7, num_orders)
}
orders_df = pd.DataFrame(orders_data)

# Save orders_df in session state to simulate real-time updates
if "orders_df" not in st.session_state:
    st.session_state["orders_df"] = orders_df

# Sidebar for filtering
st.sidebar.header("Filters")
selected_hub = st.sidebar.selectbox("Select Hub", options=["All"] + list(range(1, num_hubs + 1)))
selected_status = st.sidebar.selectbox("Select Status", options=["All", "Delivered", "In Transit", "Pending"])
selected_driver = st.sidebar.selectbox("Select Driver", options=["All"] + list(range(1, num_drivers + 1)))

# Apply filters
filtered_df = st.session_state["orders_df"].copy()
if selected_hub != "All":
    filtered_df = filtered_df[filtered_df["Hub_ID"] == int(selected_hub)]
if selected_status != "All":
    filtered_df = filtered_df[filtered_df["Status"] == selected_status]
if selected_driver != "All":
    filtered_df = filtered_df[filtered_df["Driver_ID"] == int(selected_driver)]

# Display filtered data
st.subheader("Filtered Orders Data")
st.dataframe(filtered_df)

# KPI Metrics
st.subheader("Key Performance Indicators (KPIs)")
col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", len(filtered_df))
col2.metric("Average Delivery Time", f"{filtered_df['Delivery_Time_Minutes'].mean():.2f} mins")
col3.metric("Total Order Value", f"${filtered_df['Order_Value'].sum():.2f}")

# Simulate real-time updates
st.subheader("Real-Time Order Updates")
if st.button("Simulate Order Status Update"):
    # Randomly update the status of 10 orders
    indices_to_update = np.random.choice(st.session_state["orders_df"].index, size=10, replace=False)
    new_statuses = np.random.choice(["Delivered", "In Transit", "Pending"], size=10)
    st.session_state["orders_df"].loc[indices_to_update, "Status"] = new_statuses
    st.success("Order statuses updated!")

# Map Visualization
st.subheader("Hub and Delivery Locations Map")
m = folium.Map(location=[13.0, 77.6], zoom_start=12)

# Add hubs to the map
for hub_id, (lat, lon) in hub_locations.items():
    folium.Marker(
        [lat, lon],
        popup=f"Hub {hub_id}",
        icon=folium.Icon(color="blue", icon="warehouse")
    ).add_to(m)

# Add filtered customer delivery locations
for _, row in filtered_df.iterrows():
    folium.Marker(
        [row["Customer_Lat"], row["Customer_Lon"]],
        popup=f"Order {row['Order_ID']} - Status: {row['Status']}",
        icon=folium.Icon(color="green" if row["Status"] == "Delivered" else "orange", icon="box")
    ).add_to(m)

# Display the map
st_folium(m, width=700, height=500)

# Visualizations
st.subheader("Visual Insights")

# 1. Orders Distribution Across Hubs
st.write("### Orders Distribution Across Hubs")
orders_per_hub = st.session_state["orders_df"].groupby("Hub_ID").size().reset_index(name="Order_Count")
fig1 = px.bar(orders_per_hub, x="Hub_ID", y="Order_Count", title="Orders per Hub", color="Order_Count")
st.plotly_chart(fig1, use_container_width=True)

# 2. Delivery Status Distribution
st.write("### Delivery Status Distribution")
status_counts = filtered_df["Status"].value_counts().reset_index()
status_counts.columns = ["Status", "Count"]
fig2 = px.pie(status_counts, names="Status", values="Count", title="Order Status Breakdown")
st.plotly_chart(fig2, use_container_width=True)

# 3. Delivery Time Distribution
st.write("### Delivery Time Distribution")
fig3, ax3 = plt.subplots()
sns.histplot(filtered_df["Delivery_Time_Minutes"], bins=20, kde=True, ax=ax3)
ax3.set_title("Delivery Time Distribution (Minutes)")
ax3.set_xlabel("Delivery Time (Minutes)")
ax3.set_ylabel("Frequency")
st.pyplot(fig3)

# 4. Driver Workload
st.write("### Driver Workload")
orders_per_driver = filtered_df.groupby("Driver_ID").size().reset_index(name="Order_Count")
fig4 = px.bar(orders_per_driver, x="Driver_ID", y="Order_Count", title="Orders per Driver", color="Order_Count")
st.plotly_chart(fig4, use_container_width=True)

# 5. Driver Performance Analytics
st.write("### Driver Performance Analytics")
driver_performance = filtered_df.groupby("Driver_ID").agg({
    "Delivery_Time_Minutes": "mean",
    "Order_Value": "sum",
    "Order_ID": "count"
}).reset_index()
driver_performance.columns = ["Driver_ID", "Avg_Delivery_Time", "Total_Order_Value", "Total_Orders"]
fig5 = px.scatter(driver_performance, x="Avg_Delivery_Time", y="Total_Orders", size="Total_Order_Value",
                  color="Driver_ID", title="Driver Performance (Bubble Size = Total Order Value)")
st.plotly_chart(fig5, use_container_width=True)

# 6. Order Value by Hub
st.write("### Order Value by Hub")
order_value_per_hub = filtered_df.groupby("Hub_ID")["Order_Value"].sum().reset_index()
fig6 = px.bar(order_value_per_hub, x="Hub_ID", y="Order_Value", title="Total Order Value per Hub", color="Order_Value")
st.plotly_chart(fig6, use_container_width=True)

# Order Assignment Optimization (Simple heuristic: Assign to least busy driver)
st.subheader("Order Assignment Optimization")
if st.button("Suggest Driver Assignments"):
    # Calculate current workload of drivers
    driver_workload = filtered_df.groupby("Driver_ID").size().to_dict()
    # Suggest least busy driver for each hub
    suggestions = {}
    for hub_id in range(1, num_hubs + 1):
        least_busy_driver = min(driver_workload, key=driver_workload.get)
        suggestions[hub_id] = least_busy_driver
        # Simulate assigning more work to this driver
        driver_workload[least_busy_driver] += 1
    st.write("### Suggested Driver Assignments for Hubs")
    st.write(suggestions)

# Export Filtered Data
st.subheader("Export Data")
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_orders.csv",
    mime="text/csv"
)

# Simulate Email Notifications
st.subheader("Send Email Notifications")
recipient_email = st.text_input("Recipient Email", "example@example.com")
if st.button("Send Order Update Notification"):
    try:
        msg = MIMEText("Order updates:\n" + filtered_df.head().to_string())
        msg["Subject"] = "Quick Commerce Order Update"
        msg["From"] = "sender@example.com"
        msg["To"] = recipient_email
        # Simulate sending email (Actual SMTP server setup required)
        st.success(f"Simulated sending email to {recipient_email}")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# Footer
st.markdown("---")
st.write("Built with ❤️ using Streamlit")

