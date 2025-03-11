import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(page_title="AutoTwin Dashboard", layout="wide", initial_sidebar_state="expanded")

# Sample Data Generation (Simulating real-time and historical data)
np.random.seed(42)
timestamps = pd.date_range(start="2023-10-01", periods=500, freq="H")
data = pd.DataFrame({
    "timestamp": timestamps,
    "temperature": np.random.normal(70, 5, 500),
    "pressure": np.random.normal(30, 2, 500),
    "throughput": np.random.randint(50, 100, 500),
    "defect_rate": np.random.uniform(0, 5, 500),
    "machine_status": np.random.choice(["Active", "Idle", "Maintenance"], 500)
})

# Predictive Maintenance Data (Fixing the error by using a DataFrame instead of a dict)
predictive_data = pd.DataFrame({
    "Machine": ["Machine A", "Machine B", "Machine C"],
    "Failure_Likelihood": [0.7, 0.3, 0.9]
})

# Simulated Alerts Data
alerts_data = pd.DataFrame({
    "Timestamp": [datetime.now() - timedelta(minutes=i*60) for i in range(5)],
    "Alert": ["Temperature High", "Pressure Low", "Defect Rate High", "Motor Failure", "Conveyor Jam"],
    "Severity": ["High", "Medium", "High", "Critical", "Medium"]
})

# Sidebar Navigation
st.sidebar.title("AutoTwin Dashboard")
st.sidebar.markdown("### Navigation")
page = st.sidebar.selectbox("Select Feature", [
    "Real-Time Monitoring",
    "Predictive Maintenance",
    "Scenario Simulation",
    "Historical Data",
    "Alerts & Notifications"
])

# Main Title
st.title("🚗 AutoTwin Dashboard for Automobile Manufacturing")

# Page 1: Real-Time Monitoring
if page == "Real-Time Monitoring":
    st.header("Real-Time Monitoring")
    
    # KPI Widgets
    st.markdown("### Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Throughput", f"{int(data['throughput'].iloc[-1])} units/hr", "+5%")
    with col2:
        st.metric("Downtime", "2 hrs", "-10%")
    with col3:
        st.metric("Defect Rate", f"{data['defect_rate'].iloc[-1]:.2f}%", "-0.2%")
    
    # Time-Series Charts
    st.markdown("### Sensor Data Trends")
    fig_temp = px.line(data, x="timestamp", y="temperature", title="Temperature Over Time")
    st.plotly_chart(fig_temp, use_container_width=True)
    
    fig_pressure = px.line(data, x="timestamp", y="pressure", title="Pressure Over Time")
    st.plotly_chart(fig_pressure, use_container_width=True)

    # Machine Status Pie Chart
    st.markdown("### Machine Status Distribution")
    status_counts = data["machine_status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    fig_pie = px.pie(status_counts, names="Status", values="Count", title="Machine Status")
    st.plotly_chart(fig_pie, use_container_width=True)

    # Production Line Schematic (Placeholder)
    st.markdown("### Production Line Schematic")
    st.image("https://github.com/aniketd0613/dtwin_Eureka/blob/main/schematic.png", caption="Live Production Line")

# Page 2: Predictive Maintenance
elif page == "Predictive Maintenance":
    st.header("Predictive Maintenance")
    
    # Bar Chart for Failure Likelihood (Fixed error by using DataFrame)
    st.markdown("### Likelihood of Failure for Machines")
    fig_bar = px.bar(predictive_data, x="Machine", y="Failure_Likelihood", 
                     title="Failure Likelihood", color="Failure_Likelihood", 
                     range_y=[0, 1], labels={"Failure_Likelihood": "Probability"})
    st.plotly_chart(fig_bar, use_container_width=True)

    # Gauges for Each Machine
    st.markdown("### Machine Health Gauges")
    cols = st.columns(3)
    for i, row in predictive_data.iterrows():
        with cols[i]:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=row["Failure_Likelihood"] * 100,
                title={'text': row["Machine"]},
                gauge={'axis': {'range': [0, 100]},
                       'bar': {'color': "darkblue"},
                       'steps': [
                           {'range': [0, 50], 'color': "green"},
                           {'range': [50, 75], 'color': "yellow"},
                           {'range': [75, 100], 'color': "red"}]}
            ))
            st.plotly_chart(fig_gauge, use_container_width=True)

    # Recommendations Table
    st.markdown("### Maintenance Recommendations")
    recommendations = pd.DataFrame({
        "Machine": ["Machine A", "Machine B", "Machine C"],
        "Recommendation": ["Schedule maintenance in 48 hrs", "Monitor closely", "Immediate action required"]
    })
    st.table(recommendations)

# Page 3: Scenario Simulation
elif page == "Scenario Simulation":
    st.header("Scenario Simulation")
    
    # Input Sliders for Simulation
    st.markdown("### Adjust Parameters")
    speed = st.slider("Production Speed (units/hr)", 50, 150, 100)
    workforce = st.slider("Workforce Size", 10, 50, 30)
    
    # Simulated Results
    simulated_throughput = speed * 1.2
    simulated_cost = workforce * 500
    simulated_defect_rate = 5 - (speed * 0.02)

    # Display Results
    st.markdown("### Simulated Results")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Simulated Throughput", f"{simulated_throughput:.1f} units/hr")
    with col2:
        st.metric("Estimated Cost", f"${simulated_cost:,}")
    with col3:
        st.metric("Simulated Defect Rate", f"{simulated_defect_rate:.2f}%")

    # Radar Chart for Comparison
    st.markdown("### Current vs Simulated Metrics")
    radar_data = pd.DataFrame({
        "Metric": ["Throughput", "Cost", "Defect Rate"],
        "Current": [100, 15000, 2.5],
        "Simulated": [simulated_throughput, simulated_cost / 1000, simulated_defect_rate]
    })
    fig_radar = px.line_polar(radar_data, r="Current", theta="Metric", line_close=True, 
                              title="Current Metrics", color_discrete_sequence=["blue"])
    fig_radar.add_trace(go.Scatterpolar(r=radar_data["Simulated"], theta=radar_data["Metric"], 
                                        fill="toself", name="Simulated", line=dict(color="red")))
    st.plotly_chart(fig_radar, use_container_width=True)

# Page 4: Historical Data
elif page == "Historical Data":
    st.header("Historical Data Analysis")
    
    # Date Range Filter
    st.markdown("### Select Date Range")
    date_range = st.date_input("Date Range", [data["timestamp"].min(), data["timestamp"].max()])
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_data = data[(data["timestamp"] >= pd.to_datetime(start_date)) & 
                            (data["timestamp"] <= pd.to_datetime(end_date))]
        
        # Line Chart for Trends
        st.markdown("### Trends Over Time")
        fig_line = px.line(filtered_data, x="timestamp", y=["throughput", "defect_rate"], 
                           title="Throughput and Defect Rate Trends")
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Heatmap for Defect Rates
        st.markdown("### Defect Rate Heatmap")
        heatmap_data = filtered_data.pivot_table(index=filtered_data["timestamp"].dt.hour, 
                                                columns=filtered_data["timestamp"].dt.day, 
                                                values="defect_rate", aggfunc="mean")
        fig, ax = plt.subplots()
        sns.heatmap(heatmap_data, cmap="YlOrRd", ax=ax)
        st.pyplot(fig)

        # Export Data Button
        st.markdown("### Export Data")
        csv = filtered_data.to_csv(index=False)
        st.download_button("Download CSV", csv, "historical_data.csv", "text/csv")

# Page 5: Alerts & Notifications
elif page == "Alerts & Notifications":
    st.header("Alerts & Notifications")
    
    # Alerts Timeline
    st.markdown("### Alerts Timeline")
    fig_timeline = px.scatter(alerts_data, x="Timestamp", y="Severity", color="Severity", 
                              size=[10]*len(alerts_data), text="Alert", 
                              title="Alerts Timeline")
    st.plotly_chart(fig_timeline, use_container_width=True)

    # Alerts Table
    st.markdown("### Recent Alerts")
    st.table(alerts_data)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by Team Eureka")
