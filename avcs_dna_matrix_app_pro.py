# avcs_dna_matrix_app_pro.py - AVCS DNA Industrial Monitor v6.0 (STABLE)
import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AVCS DNA Matrix Soul v6.0",
    layout="wide",
    page_icon="🏭"
)

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
        'DAMPER_FL': 'Front-Left (LORD RD-8040)',
        'DAMPER_FR': 'Front-Right (LORD RD-8040)',
        'DAMPER_RL': 'Rear-Left (LORD RD-8040)',
        'DAMPER_RR': 'Rear-Right (LORD RD-8040)'
    }
    VIBRATION_LIMITS = {'normal': 2.0, 'warning': 4.0, 'critical': 6.0}
    TEMPERATURE_LIMITS = {'normal': 70, 'warning': 85, 'critical': 100}
    NOISE_LIMITS = {'normal': 70, 'warning': 85, 'critical': 100}
    DAMPER_FORCES = {'standby': 500, 'normal': 1000, 'warning': 4000, 'critical': 8000}

# --- FAILURE MODES ---
FAILURE_MODES = {
    "normal": {"name": "🟢 Normal Operation", "vib": 1.0, "temp": 65, "noise": 65},
    "bearing_wear": {"name": "🟠 Bearing Wear", "vib": 5.0, "temp": 80, "noise": 75},
    "misalignment": {"name": "🔴 Shaft Misalignment", "vib": 6.0, "temp": 75, "noise": 70},
    "imbalance": {"name": "🟣 Rotational Imbalance", "vib": 7.0, "temp": 70, "noise": 80},
    "cavitation": {"name": "🔵 Pump Cavitation", "vib": 3.0, "temp": 68, "noise": 90}
}

# --- INITIALIZATION ---
def initialize_system():
    if "system_running" not in st.session_state:
        st.session_state.system_running = False
    if "current_mode" not in st.session_state:
        st.session_state.current_mode = "normal"
    if "vibration_data" not in st.session_state:
        st.session_state.vibration_data = pd.DataFrame(columns=list(IndustrialConfig.VIBRATION_SENSORS.keys()))
    if "temperature_data" not in st.session_state:
        st.session_state.temperature_data = pd.DataFrame(columns=list(IndustrialConfig.THERMAL_SENSORS.keys()))
    if "noise_data" not in st.session_state:
        st.session_state.noise_data = pd.DataFrame(columns=['NOISE'])
    if "damper_data" not in st.session_state:
        st.session_state.damper_data = pd.DataFrame(columns=list(IndustrialConfig.MR_DAMPERS.keys()))
    if "risk_history" not in st.session_state:
        st.session_state.risk_history = []
    if "current_cycle" not in st.session_state:
        st.session_state.current_cycle = 0
    if "damper_forces" not in st.session_state:
        st.session_state.damper_forces = {damper: 500 for damper in IndustrialConfig.MR_DAMPERS.keys()}

# --- SENSOR DATA GENERATION ---
def generate_sensor_data(cycle, failure_mode):
    mode_data = FAILURE_MODES[failure_mode]
    
    # Vibration data
    vibration = {}
    for i, sensor in enumerate(IndustrialConfig.VIBRATION_SENSORS.keys()):
        base_vib = mode_data["vib"]
        variation = 0.2 + i * 0.1
        vibration[sensor] = max(0.1, base_vib + np.random.normal(0, variation))
    
    # Temperature data
    temperature = {}
    for i, sensor in enumerate(IndustrialConfig.THERMAL_SENSORS.keys()):
        base_temp = mode_data["temp"]
        variation = 1.0 + i * 0.5
        temperature[sensor] = max(20, base_temp + np.random.normal(0, variation))
    
    # Noise data
    base_noise = mode_data["noise"]
    noise = max(30, base_noise + np.random.normal(0, 2))
    
    return vibration, temperature, noise

# --- CALCULATIONS ---
def calculate_risk(vibration, temperature, noise):
    max_vib = max(vibration.values()) if vibration else 0
    max_temp = max(temperature.values()) if temperature else 0
    
    risk = 0
    if max_vib > 6.0:
        risk += 60
    elif max_vib > 4.0:
        risk += 40
    elif max_vib > 2.0:
        risk += 20
        
    if max_temp > 95:
        risk += 50
    elif max_temp > 85:
        risk += 30
    elif max_temp > 75:
        risk += 15
        
    if noise > 95:
        risk += 40
    elif noise > 85:
        risk += 25
    elif noise > 75:
        risk += 10
        
    return min(100, risk)

def calculate_rul(risk_index, cycle):
    base_rul = 100 - risk_index
    if cycle > 50:
        base_rul -= (cycle - 50) * 0.1
    return max(0, int(base_rul))

def calculate_damper_force(risk_index):
    if risk_index > 80:
        return IndustrialConfig.DAMPER_FORCES['critical']
    elif risk_index > 50:
        return IndustrialConfig.DAMPER_FORCES['warning']
    elif risk_index > 20:
        return IndustrialConfig.DAMPER_FORCES['normal']
    else:
        return IndustrialConfig.DAMPER_FORCES['standby']

# --- VISUALIZATIONS ---
def create_sensor_chart(data, title, y_title):
    fig = go.Figure()
    if not data.empty:
        for column in data.columns:
            fig.add_trace(go.Scatter(
                y=data[column],
                name=column,
                line=dict(width=2),
                mode='lines'
            ))
    fig.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title=y_title,
        height=250,
        showlegend=True
    )
    return fig

def create_risk_gauge(risk_index):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_index,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Risk Index"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 20], 'color': 'lightgreen'},
                {'range': [20, 50], 'color': 'yellow'},
                {'range': [50, 80], 'color': 'orange'},
                {'range': [80, 100], 'color': 'red'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': risk_index
            }
        }
    ))
    fig.update_layout(height=250)
    return fig

# --- MAIN APPLICATION ---
def main():
    initialize_system()
    
    st.title("🏭 AVCS DNA Matrix Soul v6.0")
    st.markdown("**Industrial Monitoring System with Predictive Maintenance**")
    
    # Sidebar
    st.sidebar.header("🎛️ Control Panel")
    
    # Failure mode selection
    st.sidebar.subheader("🔧 Failure Mode")
    for mode_key, mode_data in FAILURE_MODES.items():
        if st.sidebar.button(mode_data["name"], use_container_width=True):
            st.session_state.current_mode = mode_key
            st.rerun()
    
    st.sidebar.write(f"**Active:** {FAILURE_MODES[st.session_state.current_mode]['name']}")
    
    # Control buttons
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("⚡ Start System", type="primary", use_container_width=True):
            st.session_state.system_running = True
            st.session_state.vibration_data = pd.DataFrame(columns=list(IndustrialConfig.VIBRATION_SENSORS.keys()))
            st.session_state.temperature_data = pd.DataFrame(columns=list(IndustrialConfig.THERMAL_SENSORS.keys()))
            st.session_state.noise_data = pd.DataFrame(columns=['NOISE'])
            st.session_state.damper_data = pd.DataFrame(columns=list(IndustrialConfig.MR_DAMPERS.keys()))
            st.session_state.risk_history = []
            st.session_state.current_cycle = 0
            st.rerun()
    
    with col2:
        if st.button("🛑 Stop System", use_container_width=True):
            st.session_state.system_running = False
            st.session_state.damper_forces = {damper: 500 for damper in IndustrialConfig.MR_DAMPERS.keys()}
            st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Settings")
    simulation_speed = st.sidebar.slider("Speed", 0.1, 2.0, 0.5, 0.1)
    max_cycles = st.sidebar.slider("Max Cycles", 50, 500, 200, 50)
    
    # Status
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Status")
    status_display = st.sidebar.empty()
    cycle_display = st.sidebar.empty()
    progress_display = st.sidebar.empty()
    
    # Main display
    if not st.session_state.system_running:
        show_landing_page()
    else:
        run_monitoring_loop(status_display, cycle_display, progress_display, simulation_speed, max_cycles)

def show_landing_page():
    st.info("🚀 **System Ready** - Select failure mode and click 'Start System'")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📊 Monitoring")
        st.write("• 4x Vibration Sensors")
        st.write("• 4x Thermal Sensors")
        st.write("• Acoustic Monitoring")
        st.write("• Real-time Analytics")
    
    with col2:
        st.subheader("🛡️ Protection")
        st.write("• 4x MR Dampers")
        st.write("• Active Vibration Control")
        st.write("• Emergency Shutdown")
        st.write("• Safety Limits")
    
    with col3:
        st.subheader("🔧 Features")
        st.write("• 5 Failure Modes")
        st.write("• Predictive Maintenance")
        st.write("• Risk Assessment")
        st.write("• RUL Calculation")

def run_monitoring_loop(status_display, cycle_display, progress_display, speed, max_cycles):
    current_cycle = st.session_state.current_cycle
    
    if current_cycle < max_cycles and st.session_state.system_running:
        # Generate data
        vibration, temperature, noise = generate_sensor_data(current_cycle, st.session_state.current_mode)
        
        # Calculate metrics
        risk_index = calculate_risk(vibration, temperature, noise)
        rul_hours = calculate_rul(risk_index, current_cycle)
        damper_force = calculate_damper_force(risk_index)
        
        # Update damper forces
        st.session_state.damper_forces = {damper: damper_force for damper in IndustrialConfig.MR_DAMPERS.keys()}
        
        # Store data
        st.session_state.vibration_data = pd.concat([
            st.session_state.vibration_data,
            pd.DataFrame([vibration])
        ], ignore_index=True)
        
        st.session_state.temperature_data = pd.concat([
            st.session_state.temperature_data,
            pd.DataFrame([temperature])
        ], ignore_index=True)
        
        st.session_state.noise_data = pd.concat([
            st.session_state.noise_data,
            pd.DataFrame([{'NOISE': noise}])
        ], ignore_index=True)
        
        st.session_state.damper_data = pd.concat([
            st.session_state.damper_data,
            pd.DataFrame([st.session_state.damper_forces])
        ], ignore_index=True)
        
        st.session_state.risk_history.append(risk_index)
        
        # Limit data size
        if len(st.session_state.vibration_data) > 50:
            st.session_state.vibration_data = st.session_state.vibration_data.iloc[1:]
        if len(st.session_state.temperature_data) > 50:
            st.session_state.temperature_data = st.session_state.temperature_data.iloc[1:]
        if len(st.session_state.noise_data) > 50:
            st.session_state.noise_data = st.session_state.noise_data.iloc[1:]
        if len(st.session_state.damper_data) > 50:
            st.session_state.damper_data = st.session_state.damper_data.iloc[1:]
        if len(st.session_state.risk_history) > 50:
            st.session_state.risk_history = st.session_state.risk_history[1:]
        
        # Update displays
        update_displays(risk_index, rul_hours, current_cycle, max_cycles, status_display, cycle_display, progress_display)
        
        # Next cycle
        st.session_state.current_cycle += 1
        time.sleep(speed)
        st.rerun()
    
    elif current_cycle >= max_cycles:
        st.success("✅ Simulation completed!")
        st.session_state.system_running = False

def update_displays(risk_index, rul_hours, current_cycle, max_cycles, status_display, cycle_display, progress_display):
    # Status
    if risk_index > 80:
        status_text = "🚨 CRITICAL"
        status_color = "red"
    elif risk_index > 50:
        status_text = "⚠️ WARNING"
        status_color = "orange"
    elif risk_index > 20:
        status_text = "✅ NORMAL"
        status_color = "green"
    else:
        status_text = "🟢 STANDBY"
        status_color = "blue"
    
    status_display.markdown(f"<h3 style='color: {status_color};'>{status_text}</h3>", unsafe_allow_html=True)
    cycle_display.metric("Cycle", f"{current_cycle + 1}/{max_cycles}")
    progress_display.progress((current_cycle + 1) / max_cycles)
    
    # Dashboard
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Sensor charts
        st.subheader("📈 Sensor Monitoring")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Vibration", "Temperature", "Noise", "Dampers"])
        
        with tab1:
            if not st.session_state.vibration_data.empty:
                st.plotly_chart(create_sensor_chart(
                    st.session_state.vibration_data, 
                    "Vibration Sensors", "Vibration (mm/s)"
                ), use_container_width=True)
        
        with tab2:
            if not st.session_state.temperature_data.empty:
                st.plotly_chart(create_sensor_chart(
                    st.session_state.temperature_data,
                    "Temperature Sensors", "Temperature (°C)"
                ), use_container_width=True)
        
        with tab3:
            if not st.session_state.noise_data.empty:
                st.plotly_chart(create_sensor_chart(
                    st.session_state.noise_data,
                    "Noise Level", "Noise (dB)"
                ), use_container_width=True)
        
        with tab4:
            if not st.session_state.damper_data.empty:
                st.plotly_chart(create_sensor_chart(
                    st.session_state.damper_data,
                    "MR Damper Forces", "Force (N)"
                ), use_container_width=True)
    
    with col2:
        st.subheader("🎯 System Metrics")
        
        # Risk gauge
        st.plotly_chart(create_risk_gauge(risk_index), use_container_width=True)
        
        # Metrics
        col_a, col_b = st.columns(2)
        with col_a:
            if rul_hours < 24:
                st.error(f"⏳ RUL\n{rul_hours}h")
            elif rul_hours < 72:
                st.warning(f"⏳ RUL\n{rul_hours}h")
            else:
                st.success(f"⏳ RUL\n{rul_hours}h")
            
            st.metric("🔄 Cycle", current_cycle + 1)
        
        with col_b:
            st.metric("📊 Risk", f"{risk_index}%")
            st.metric("🔧 Mode", FAILURE_MODES[st.session_state.current_mode]['name'])
        
        # Damper status
        st.subheader("🔄 MR Dampers")
        damper_cols = st.columns(2)
        dampers_list = list(IndustrialConfig.MR_DAMPERS.items())
        
        for i, (damper, name) in enumerate(dampers_list):
            with damper_cols[i % 2]:
                force = st.session_state.damper_forces[damper]
                if force >= 4000:
                    st.error(f"🔴 {name}\n{force}N")
                elif force >= 1000:
                    st.warning(f"🟡 {name}\n{force}N")
                else:
                    st.success(f"🟢 {name}\n{force}N")

if __name__ == "__main__":
    main()
