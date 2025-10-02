# thermal_dna_app.py - Thermal DNA Fusion Simulator v2.0
import streamlit as st
import numpy as np
import pandas as pd
import time

# --- CONFIG ---
st.set_page_config(page_title="Thermal DNA Fusion", layout="wide")

# --- HEADER ---
st.title("🌡️⚙️ Thermal DNA Fusion Simulator")
st.markdown("**Real-time thermal & vibration monitoring for FPSO equipment (AVCS DNA)**")

# --- STATE INIT ---
if "running" not in st.session_state:
    st.session_state.running = False
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Temperature", "Vibration"])
if "cycle" not in st.session_state:
    st.session_state.cycle = 0

# --- CONTROLS ---
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start Simulation", type="primary"):
        st.session_state.running = True
        st.session_state.data = pd.DataFrame(columns=["Temperature", "Vibration"])
        st.session_state.cycle = 0
with col2:
    if st.button("⏹️ Stop Simulation"):
        st.session_state.running = False

# --- DASHBOARD ---
placeholder_chart = st.empty()
status_box = st.empty()
progress_bar = st.progress(0)

# --- MAIN LOOP ---
if st.session_state.running:
    for cycle in range(50):
        if not st.session_state.running:
            break

        # Генерация данных
        if cycle < 20:
            temp = 55 + np.random.normal(0, 2)
            vib = 1.0 + np.random.normal(0, 0.1)
        elif cycle < 40:
            temp = 70 + np.random.normal(0, 3)
            vib = 2.5 + np.random.normal(0, 0.2)
        else:
            temp = 90 + np.random.normal(0, 4)
            vib = 4.0 + np.random.normal(0, 0.3)

        # Запись в таблицу
        st.session_state.data.loc[cycle] = [temp, vib]

        # --- График (температура + вибрация) ---
        with placeholder_chart.container():
            st.subheader("📈 Real-Time Sensor Data")
            st.line_chart(st.session_state.data, height=300)

        # --- Логика риска ---
        risk_level = "✅ NORMAL"
        msg = f"Temp: {temp:.1f}°C | Vib: {vib:.2f} mm/s"

        if temp > 80 or vib > 3.5:
            risk_level = "🚨 CRITICAL"
            status_box.error(f"{risk_level} | {msg} - Immediate action required!")
        elif temp > 60 or vib > 2.0:
            risk_level = "⚠️ WARNING"
            status_box.warning(f"{risk_level} | {msg} - Monitor closely")
        else:
            status_box.success(f"{risk_level} | {msg}")

        # --- Прогресс ---
        progress_bar.progress((cycle + 1) / 50)
        st.session_state.cycle = cycle

        time.sleep(0.5)

# --- SIDEBAR INFO ---
st.sidebar.header("System Info")
st.sidebar.write("**Thermal DNA Fusion** - Predictive maintenance for FPSO")
st.sidebar.write("**Sensors:** 8 thermal + 4 vibration")
st.sidebar.write("**Sampling:** 1 Hz")
st.sidebar.write("**AI Analysis:** Real-time anomaly detection")

st.markdown("---")
st.caption("Thermal DNA Fusion Simulator v2.0 | AVCS DNA Monitoring System")
