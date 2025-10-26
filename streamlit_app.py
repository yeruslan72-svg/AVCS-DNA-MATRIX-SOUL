# streamlit_app.py - AVCS DNA Industrial Monitor
import streamlit as st
import numpy as np
import pandas as pd
import time
from sklearn.ensemble import IsolationForest
import plotly.graph_objects as go

# --- FIXED CONFIG ---
try:
    st.set_page_config(page_title="AVCS DNA Monitor", layout="wide")
except:
    pass

# --- SYSTEM CONFIG ---
class IndustrialConfig:
    VIBRATION_SENSORS = {
        'VIB_MOTOR_DRIVE': 'Motor Drive End',
        'VIB_MOTOR_NONDRIVE': 'Motor Non-Drive End', 
        'VIB_PUMP_INLET': 'Pump Inlet Bearing',
        'VIB_PUMP_OUTLET': 'Pump Outlet Bearing'
    }
    THERMAL_SENSORS = {
        'TEMP_MOTOR_WINDING': 'Motor Winding',
        'TEMP_MOTOR_BEARING': 'Motor Bearing',
        'TEMP_PUMP_BEARING': 'Pump Bearing', 
        'TEMP_PUMP_CASING': 'Pump Casing'
    }
    MR_DAMPERS = {
        'DAMPER_FL': 'Front-Left',
        'DAMPER_FR': 'Front-Right', 
        'DAMPER_RL': 'Rear-Left',
        'DAMPER_RR': 'Rear-Right'
    }
    ACOUSTIC_SENSOR = "Pump Acoustic Noise (dB)"
    VIBRATION_LIMITS = {'normal': 2.0, 'warning': 4.0, 'critical': 6.0}
    TEMPERATURE_LIMITS = {'normal': 70, 'warning': 85, 'critical': 100}
    DAMPER_FORCES = {'standby': 500, 'normal': 1000, 'warning': 4000, 'critical': 8000}

# --- INIT SESSION ---
if "system_running" not in st.session_state:
    st.session_state.system_running = False
if "vibration_data" not in st.session_state:
    st.session_state.vibration_data = pd.DataFrame(columns=list(IndustrialConfig.VIBRATION_SENSORS.keys()))
if "temperature_data" not in st.session_state:
    st.session_state.temperature_data = pd.DataFrame(columns=list(IndustrialConfig.THERMAL_SENSORS.keys()))
if "noise_data" not in st.session_state:
    st.session_state.noise_data = pd.DataFrame(columns=[IndustrialConfig.ACOUSTIC_SENSOR])
if "risk_history" not in st.session_state:
    st.session_state.risk_history = []
if "current_cycle" not in st.session_state:
    st.session_state.current_cycle = 0

# --- HEADER ---
st.title("🏭 AVCS DNA Industrial Monitor")
st.markdown("**AI-Powered Predictive Maintenance**")

# --- SIDEBAR ---
st.sidebar.header("Control Panel")
if st.sidebar.button("⚡ Start System", type="primary"):
    st.session_state.system_running = True
    st.session_state.vibration_data = pd.DataFrame(columns=list(IndustrialConfig.VIBRATION_SENSORS.keys()))
    st.session_state.temperature_data = pd.DataFrame(columns=list(IndustrialConfig.THERMAL_SENSORS.keys()))
    st.session_state.noise_data = pd.DataFrame(columns=[IndustrialConfig.ACOUSTIC_SENSOR])
    st.session_state.risk_history = []
    st.session_state.current_cycle = 0
    st.rerun()

if st.sidebar.button("🛑 Stop System"):
    st.session_state.system_running = False
    st.rerun()

# --- MAIN APP ---
if not st.session_state.system_running:
    st.info("🚀 Click 'Start System' to begin monitoring")
else:
    # Generate sample data
    cycle = st.session_state.current_cycle
    if cycle < 50:
        vib = 1.0 + np.random.normal(0, 0.2)
        temp = 65 + np.random.normal(0, 3)
        noise = 65 + np.random.normal(0, 2)
    else:
        vib = 5.0 + np.random.normal(0, 0.5)
        temp = 90 + np.random.normal(0, 5) 
        noise = 90 + np.random.normal(0, 5)
    
    # Add to data
    new_vib = {k: max(0.1, vib + np.random.normal(0, 0.1)) for k in IndustrialConfig.VIBRATION_SENSORS.keys()}
    new_temp = {k: max(20, temp + np.random.normal(0, 2)) for k in IndustrialConfig.THERMAL_SENSORS.keys()}
    
    st.session_state.vibration_data = pd.concat([
        st.session_state.vibration_data, 
        pd.DataFrame([new_vib])
    ], ignore_index=True)
    st.session_state.temperature_data = pd.concat([
        st.session_state.temperature_data,
        pd.DataFrame([new_temp]) 
    ], ignore_index=True)
    st.session_state.noise_data = pd.concat([
        st.session_state.noise_data,
        pd.DataFrame([{IndustrialConfig.ACOUSTIC_SENSOR: noise}])
    ], ignore_index=True)
    
    # Keep only last 50 points
    if len(st.session_state.vibration_data) > 50:
        st.session_state.vibration_data = st.session_state.vibration_data.iloc[1:]
    if len(st.session_state.temperature_data) > 50:
        st.session_state.temperature_data = st.session_state.temperature_data.iloc[1:]
    if len(st.session_state.noise_data) > 50:
        st.session_state.noise_data = st.session_state.noise_data.iloc[1:]
    
    # Display
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Vibration")
        if not st.session_state.vibration_data.empty:
            st.line_chart(st.session_state.vibration_data)
        
        st.subheader("🌡️ Temperature") 
        if not st.session_state.temperature_data.empty:
            st.line_chart(st.session_state.temperature_data)
    
    with col2:
        st.subheader("🔊 Noise")
        if not st.session_state.noise_data.empty:
            st.line_chart(st.session_state.noise_data)
        
        st.subheader("Status")
        if vib > 4.0 or temp > 85:
            st.error("🚨 CRITICAL")
        elif vib > 2.0 or temp > 70:
            st.warning("⚠️ WARNING") 
        else:
            st.success("✅ NORMAL")
    
    st.session_state.current_cycle += 1
    st.sidebar.write(f"Cycle: {st.session_state.current_cycle}")
    
    if st.session_state.current_cycle >= 100:
        st.success("✅ Simulation complete!")
        st.session_state.system_running = False
    else:
        time.sleep(1)
        st.rerun()

st.markdown("---")
st.caption("AVCS DNA | Yeruslan Technologies")
