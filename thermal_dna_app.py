# thermal_dna_app.py - AVCS DNA Industrial Monitor v5.0
import streamlit as st
import numpy as np
import pandas as pd
import time
from sklearn.ensemble import IsolationForest
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="AVCS DNA Industrial Monitor", layout="wide")

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

    # New acoustic monitoring
    ACOUSTIC_SENSOR = "Pump Acoustic Noise (dB)"

    VIBRATION_LIMITS = {'normal': 2.0, 'warning': 4.0, 'critical': 6.0}
    TEMPERATURE_LIMITS = {'normal': 70, 'warning': 85, 'critical': 100}
    NOISE_LIMITS = {'normal': 70, 'warning': 85, 'critical': 100}
    DAMPER_FORCES = {'standby': 500, 'normal': 1000, 'warning': 4000, 'critical': 8000}


# --- HEADER ---
st.title("🏭 AVCS DNA - Industrial Monitoring System v5.0")
st.markdown("**Active Vibration Control System with AI-Powered Predictive Maintenance**")

# --- STATE INIT ---
if "system_running" not in st.session_state:
    st.session_state.system_running = False
if "vibration_data" not in st.session_state:
    st.session_state.vibration_data = pd.DataFrame(columns=list(IndustrialConfig.VIBRATION_SENSORS.keys()))
if "temperature_data" not in st.session_state:
    st.session_state.temperature_data = pd.DataFrame(columns=list(IndustrialConfig.THERMAL_SENSORS.keys()))
if "noise_data" not in st.session_state:
    st.session_state.noise_data = pd.DataFrame(columns=[IndustrialConfig.ACOUSTIC_SENSOR])
if "damper_forces" not in st.session_state:
    st.session_state.damper_forces = {damper: 0 for damper in IndustrialConfig.MR_DAMPERS.keys()}
if "damper_history" not in st.session_state:
    st.session_state.damper_history = pd.DataFrame(columns=list(IndustrialConfig.MR_DAMPERS.keys()))
if "ai_model" not in st.session_state:
    normal_vibration = np.random.normal(1.0, 0.3, (500, 4))
    normal_temperature = np.random.normal(65, 5, (500, 4))
    normal_noise = np.random.normal(65, 3, (500, 1))
    normal_data = np.column_stack([normal_vibration, normal_temperature, normal_noise])
    st.session_state.ai_model = IsolationForest(contamination=0.08, random_state=42, n_estimators=150)
    st.session_state.ai_model.fit(normal_data)

# --- SIDEBAR CONTROL ---
st.sidebar.header("🎛️ AVCS DNA Control Panel")
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("⚡ Start System", type="primary", use_container_width=True):
        st.session_state.system_running = True
        st.session_state.vibration_data = pd.DataFrame(columns=list(IndustrialConfig.VIBRATION_SENSORS.keys()))
        st.session_state.temperature_data = pd.DataFrame(columns=list(IndustrialConfig.THERMAL_SENSORS.keys()))
        st.session_state.noise_data = pd.DataFrame(columns=[IndustrialConfig.ACOUSTIC_SENSOR])
        st.session_state.damper_forces = {damper: IndustrialConfig.DAMPER_FORCES['standby'] for damper in IndustrialConfig.MR_DAMPERS.keys()}
        st.session_state.damper_history = pd.DataFrame(columns=list(IndustrialConfig.MR_DAMPERS.keys()))
with col2:
    if st.button("🛑 Emergency Stop", use_container_width=True):
        st.session_state.system_running = False
        st.session_state.damper_forces = {damper: 0 for damper in IndustrialConfig.MR_DAMPERS.keys()}

st.sidebar.markdown("---")
st.sidebar.subheader("📊 System Status")
status_indicator = st.sidebar.empty()

# --- DASHBOARD ---
st.subheader("📈 Vibration Monitoring")
vib_chart = st.empty()
vib_status = st.empty()

st.subheader("🌡️ Thermal Monitoring")
temp_chart = st.empty()
temp_status = st.empty()

st.subheader("🔊 Acoustic Monitoring")
noise_chart = st.empty()
noise_status = st.empty()

st.markdown("---")
st.subheader("🔄 MR Dampers Control")
damper_chart = st.empty()
damper_status_display = st.empty()

st.subheader("🤖 AI Fusion Analysis")
fusion_chart = st.empty()
risk_indicator = st.empty()
ai_confidence = st.empty()
rul_display = st.empty()

# --- MAIN LOOP ---
if st.session_state.system_running:
    progress_bar = st.sidebar.progress(0)
    cycle_counter = st.sidebar.empty()

    for cycle in range(100):
        if not st.session_state.system_running:
            break

        # --- DATA GENERATION ---
        if cycle < 30:
            vibration = {k: 1.0 + np.random.normal(0, 0.2) for k in IndustrialConfig.VIBRATION_SENSORS.keys()}
            temperature = {k: 65 + np.random.normal(0, 3) for k in IndustrialConfig.THERMAL_SENSORS.keys()}
            noise = 65 + np.random.normal(0, 2)
        elif cycle < 60:
            degradation = (cycle - 30) * 0.05
            vibration = {k: 1.0 + degradation + np.random.normal(0, 0.3) for k in IndustrialConfig.VIBRATION_SENSORS.keys()}
            temperature = {k: 65 + degradation * 2 + np.random.normal(0, 4) for k in IndustrialConfig.THERMAL_SENSORS.keys()}
            noise = 70 + degradation * 2 + np.random.normal(0, 3)
        else:
            vibration = {k: 5.0 + np.random.normal(0, 0.5) for k in IndustrialConfig.VIBRATION_SENSORS.keys()}
            temperature = {k: 95 + np.random.normal(0, 5) for k in IndustrialConfig.THERMAL_SENSORS.keys()}
            noise = 95 + np.random.normal(0, 5)

        # Save data
        st.session_state.vibration_data.loc[cycle] = vibration
        st.session_state.temperature_data.loc[cycle] = temperature
        st.session_state.noise_data.loc[cycle] = [noise]

        # AI Analysis
        features = list(vibration.values()) + list(temperature.values()) + [noise]
        ai_prediction = st.session_state.ai_model.predict([features])[0]
        ai_conf = st.session_state.ai_model.decision_function([features])[0]
        risk_index = min(100, max(0, int(abs(ai_conf) * 120)))

        # Remaining Useful Life (RUL)
        rul_hours = max(0, int(100 - risk_index * 0.9))

        # Damper control
        if ai_prediction == -1 or risk_index > 80:
            damper_force = IndustrialConfig.DAMPER_FORCES['critical']
            system_status = "🚨 CRITICAL"
            status_color = "red"
        elif risk_index > 50:
            damper_force = IndustrialConfig.DAMPER_FORCES['warning']
            system_status = "⚠️ WARNING"
            status_color = "orange"
        elif risk_index > 20:
            damper_force = IndustrialConfig.DAMPER_FORCES['normal']
            system_status = "✅ NORMAL"
            status_color = "green"
        else:
            damper_force = IndustrialConfig.DAMPER_FORCES['standby']
            system_status = "🟢 STANDBY"
            status_color = "blue"

        st.session_state.damper_forces = {d: damper_force for d in IndustrialConfig.MR_DAMPERS.keys()}
        st.session_state.damper_history.loc[cycle] = st.session_state.damper_forces

        # --- DISPLAY ---
        vib_chart.line_chart(st.session_state.vibration_data, height=200)
        with vib_status:
            for k, v in vibration.items():
                color = "🟢" if v < 2 else "🟡" if v < 4 else "🔴"
                st.write(f"{color} {IndustrialConfig.VIBRATION_SENSORS[k]}: {v:.1f} mm/s")

        temp_chart.line_chart(st.session_state.temperature_data, height=200)
        with temp_status:
            for k, v in temperature.items():
                color = "🟢" if v < 70 else "🟡" if v < 85 else "🔴"
                st.write(f"{color} {IndustrialConfig.THERMAL_SENSORS[k]}: {v:.0f} °C")

        noise_chart.line_chart(st.session_state.noise_data, height=200)
        with noise_status:
            color = "🟢" if noise < 70 else "🟡" if noise < 85 else "🔴"
            st.write(f"{color} Noise Level: {noise:.1f} dB")

        damper_chart.line_chart(st.session_state.damper_history, height=200)
        with damper_status_display:
            cols = st.columns(4)
            for i, (d, loc) in enumerate(IndustrialConfig.MR_DAMPERS.items()):
                with cols[i]:
                    force = st.session_state.damper_forces[d]
                    if force >= 4000:
                        st.error(f"🔴 {loc}\n{force} N")
                    elif force >= 1000:
                        st.warning(f"🟡 {loc}\n{force} N")
                    else:
                        st.success(f"🟢 {loc}\n{force} N")

        # Fusion Risk Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_index,
            title={'text': "Risk Index"},
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': "darkred"},
                   'steps': [
                       {'range': [0, 30], 'color': "lightgreen"},
                       {'range': [30, 60], 'color': "yellow"},
                       {'range': [60, 100], 'color': "red"}]}))
        fusion_chart.plotly_chart(fig, use_container_width=True)

        risk_indicator.metric("🔴 Risk Index", f"{risk_index}/100")
        ai_confidence.metric("🤖 AI Confidence", f"{abs(ai_conf):.2f}")
        rul_display.metric("⏳ RUL Estimate", f"{rul_hours} h")

        status_indicator.markdown(f"<h3 style='color: {status_color};'>{system_status}</h3>", unsafe_allow_html=True)

        progress_bar.progress((cycle + 1) / 100)
        cycle_counter.text(f"🔄 Cycle: {cycle+1}/100")

        time.sleep(0.3)

st.markdown("---")
st.caption("AVCS DNA Industrial Monitor v5.0 | Yeruslan Technologies")
