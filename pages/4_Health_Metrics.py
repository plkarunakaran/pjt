import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
from utils.data_manager import DataManager
from utils.helpers import init_session_state
from utils.theme import apply_theme

st.set_page_config(page_title="Health Metrics - MedPal", page_icon="📈")
apply_theme()
def main():
    init_session_state()
    data_manager = DataManager()
    
    st.title("📈 Health Metrics")
    st.markdown("Track and monitor your vital health indicators")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "📝 Record New", "📋 History"])
    
    with tab1:
        display_metrics_overview()
    
    with tab2:
        add_health_metric_form()
    
    with tab3:
        display_metrics_history()

# ------------------------------
# OVERVIEW & CHARTS
# ------------------------------
def display_metrics_overview():
    """Display overview of health metrics with charts"""
    health_metrics = st.session_state.get('health_metrics', [])
    
    if not health_metrics:
        st.info("No health metrics recorded yet. Use the 'Record New' tab to start tracking!")
        return
    
    df = pd.DataFrame(health_metrics)
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'].fillna('00:00'))
    
    # Latest values
    st.subheader("📊 Current Status")
    latest_metrics = {}
    for metric_type in ['blood_pressure', 'weight', 'heart_rate', 'blood_sugar']:
        type_data = df[df['type'] == metric_type]
        if not type_data.empty:
            latest = type_data.sort_values('datetime').iloc[-1]
            latest_metrics[metric_type] = latest
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'blood_pressure' in latest_metrics:
            bp = latest_metrics['blood_pressure']
            st.metric("Blood Pressure", f"{bp['value']}{bp['unit']}", help=f"Last recorded: {bp['date']}")
            if '/' in str(bp['value']):
                systolic = int(bp['value'].split('/')[0])
                if systolic > 140:
                    st.error("High")
                elif systolic > 120:
                    st.warning("Elevated")
                else:
                    st.success("Normal")
        else:
            st.metric("Blood Pressure", "No data")
    
    with col2:
        if 'weight' in latest_metrics:
            weight = latest_metrics['weight']
            st.metric("Weight", f"{weight['value']}{weight['unit']}", help=f"Last recorded: {weight['date']}")
        else:
            st.metric("Weight", "No data")
    
    with col3:
        if 'heart_rate' in latest_metrics:
            hr = latest_metrics['heart_rate']
            st.metric("Heart Rate", f"{hr['value']}{hr['unit']}", help=f"Last recorded: {hr['date']}")
            hr_value = int(hr['value'])
            if hr_value > 100:
                st.warning("High")
            elif hr_value < 60:
                st.info("Low")
            else:
                st.success("Normal")
        else:
            st.metric("Heart Rate", "No data")
    
    with col4:
        if 'blood_sugar' in latest_metrics:
            bs = latest_metrics['blood_sugar']
            st.metric("Blood Sugar", f"{bs['value']}{bs['unit']}", help=f"Last recorded: {bs['date']}")
            bs_value = int(bs['value'])
            if bs_value > 126:
                st.error("High")
            elif bs_value < 70:
                st.warning("Low")
            else:
                st.success("Normal")
        else:
            st.metric("Blood Sugar", "No data")
    
    # Charts
    st.markdown("---")
    st.subheader("📈 Trends")
    
    chart_type = st.selectbox("Select metric to view", ["Blood Pressure", "Weight", "Heart Rate", "Blood Sugar"])
    
    col1, col2 = st.columns(2)
    with col1:
        time_range = st.selectbox("Time Range", ["Last 7 days", "Last 30 days", "Last 90 days", "All time"])
    with col2:
        show_trend = st.checkbox("Show trend line", value=True)
    
    end_date = datetime.now()
    start_date = datetime.min
    if time_range == "Last 7 days":
        start_date = end_date - timedelta(days=7)
    elif time_range == "Last 30 days":
        start_date = end_date - timedelta(days=30)
    elif time_range == "Last 90 days":
        start_date = end_date - timedelta(days=90)
    
    filtered_df = df[df['datetime'] >= start_date]
    display_metric_chart(filtered_df, chart_type.lower().replace(' ', '_'), show_trend)

def display_metric_chart(df, metric_type, show_trend):
    """Display chart for specific metric type"""
    type_data = df[df['type'] == metric_type]
    if type_data.empty:
        st.info(f"No data available for {metric_type.replace('_', ' ').title()}")
        return
    
    chart_data = type_data.sort_values('datetime')
    
    if metric_type == 'blood_pressure':
        chart_data['systolic'] = chart_data['value'].apply(lambda x: int(str(x).split('/')[0]) if '/' in str(x) else int(x))
        chart_data['diastolic'] = chart_data['value'].apply(lambda x: int(str(x).split('/')[1]) if '/' in str(x) else 0)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=chart_data['datetime'], y=chart_data['systolic'], mode='lines+markers', name='Systolic'))
        fig.add_trace(go.Scatter(x=chart_data['datetime'], y=chart_data['diastolic'], mode='lines+markers', name='Diastolic'))
        st.plotly_chart(fig, use_container_width=True)
    else:
        chart_data['numeric_value'] = pd.to_numeric(chart_data['value'], errors='coerce')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=chart_data['datetime'], y=chart_data['numeric_value'], mode='lines+markers', name=metric_type))
        st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# ADD METRIC
# ------------------------------
def add_health_metric_form():
    st.subheader("Record New Health Metric")
    with st.form("add_health_metric_form"):
        metric_type = st.selectbox("Metric Type *", ["blood_pressure", "weight", "heart_rate", "blood_sugar"])
        value = st.text_input("Value *")
        unit = st.text_input("Unit *")
        date = st.date_input("Date *", value=datetime.now().date())
        time = st.time_input("Time", value=datetime.now().time())
        source = st.text_input("Source", value="manual")
        notes = st.text_area("Notes")
        
        submitted = st.form_submit_button("Record Metric", use_container_width=True)
        if submitted:
            new_metric = {
                'type': metric_type,
                'value': value,
                'unit': unit,
                'date': date.strftime('%Y-%m-%d'),
                'time': time.strftime('%H:%M'),
                'source': source,
                'notes': notes,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            if 'health_metrics' not in st.session_state:
                st.session_state.health_metrics = []
            st.session_state.health_metrics.append(new_metric)
            DataManager().save_health_metrics(st.session_state.health_metrics)
            st.success("✅ Health metric recorded!")
            st.rerun()

# ------------------------------
# HISTORY (EDIT + DELETE)
# ------------------------------
def display_metrics_history():
    health_metrics = st.session_state.get('health_metrics', [])
    if not health_metrics:
        st.info("No health metrics recorded yet.")
        return
    
    for i, metric in enumerate(health_metrics):
        metric_type = metric.get('type', 'unknown').replace('_', ' ').title()
        value = metric.get('value', 'Unknown')
        unit = metric.get('unit', '')
        date_str = metric.get('date', 'Unknown date')
        time_str = metric.get('time', '')
        
        with st.expander(f"{metric_type}: {value}{unit} - {date_str} {time_str}"):
            st.json(metric)  # shows all details nicely
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ Edit", key=f"edit_metric_{i}"):
                    edit_metric(i, metric)
            with col2:
                if st.button("🗑️ Delete", key=f"delete_metric_{i}"):
                    del st.session_state.health_metrics[i]
                    DataManager().save_health_metrics(st.session_state.health_metrics)
                    st.success("✅ Metric deleted!")
                    st.rerun()

def edit_metric(index, metric):
    st.subheader("✏️ Edit Health Metric")
    with st.form(f"edit_metric_form_{index}"):
        metric_type = st.text_input("Metric Type", value=metric.get("type", ""))
        value = st.text_input("Value", value=metric.get("value", ""))
        unit = st.text_input("Unit", value=metric.get("unit", ""))
        date = st.date_input("Date", value=datetime.strptime(metric.get("date", datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d"))
        time = st.time_input("Time", value=datetime.strptime(metric.get("time", "00:00"), "%H:%M").time())
        source = st.text_input("Source", value=metric.get("source", "manual"))
        notes = st.text_area("Notes", value=metric.get("notes", ""))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("💾 Save"):
                st.session_state.health_metrics[index] = {
                    "type": metric_type,
                    "value": value,
                    "unit": unit,
                    "date": date.strftime("%Y-%m-%d"),
                    "time": time.strftime("%H:%M"),
                    "source": source,
                    "notes": notes,
                    "created_at": metric.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                DataManager().save_health_metrics(st.session_state.health_metrics)
                st.success("✅ Metric updated!")
                st.rerun()
        with col2:
            if st.form_submit_button("❌ Cancel"):
                st.rerun()

if __name__ == "__main__":
    main()
