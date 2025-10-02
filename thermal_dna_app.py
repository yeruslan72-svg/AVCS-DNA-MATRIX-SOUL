# thermal_dna_app.py - Thermal DNA Fusion Simulator v3.0 (with AI Anomaly Detection)
import streamlit as st
import numpy as np
import pandas as pd
import time
from sklearn.ensemble import IsolationForest

# --- CONFIG ---
st.set_page_config(page_title="Thermal DNA Fusion + AI", layout="wide")

# --- HEADER ---
st.title("🌡️🤖 Thermal DNA Fusion Simulator (AVCS DNA)")
st.markdown("**Real-time thermal & vibration monitoring with AI anomaly detection**")

# --- STATE INIT ---
if "running" not in st.session_state:
    st.session_state.running = False
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Temperature", "Vibration"])
if "cycle" not in st.session_state:
    st.session_state.cycle = 0
if "model" not in st.session_state:
    # Обучаем простую модель на "нормальных" данных (50°C и 1.0 mm/s)
    normal_data = np.column_stack([
        np.random.normal(55, 2, 200),   # нормальная температура
        np.random.normal(1.0, 0.2, 200) # нормальная вибрация
    ])
    st.session_state.model = IsolationForest(contamination=0.1, random_state=42)
    st.session_state.model.fit(normal_data)

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

# --- DASHBOARD PLACEHOLDERS ---
placeholder_chart = st.empty()
status_box = st.empty()
fusion_box = st.empty()
progress_bar = st.progress(0)

# --- MAIN LOOP ---
if st.session_state.running:
    for cycle in range(50):
        if not st.session_state.running:
            break

        # Симуляция данных
        if cycle < 20:
            temp = 55 + np.random.normal(0, 2)
            vib = 1.0 + np.random.normal(0, 0.1)
        elif cycle < 40:
            temp = 70 + np.random.normal(0, 3)
            vib = 2.5 + np.random.normal(0, 0.2)
        else:
            temp = 90 + np.random.normal(0, 4)
            vib = 4.0 + np.random.normal(0, 0.3)

        # Сохраняем в DataFrame
        st.session_state.data.loc[cycle] = [temp, vib]

        # --- AI-анализ (Isolation Forest) ---
        sample = np.array([[temp, vib]])
        prediction = st.session_state.model.predict(sample)[0]  # -1 = аномалия, 1 = норма
        anomaly_score = st.session_state.model.decision_function(sample)[0]

        # Fusion Risk Index (0-100)
        risk_index = min(100, max(0, int((abs(anomaly_score) * 100))))

        # --- Визуализация ---
        with placeholder_chart.container():
            st.subheader("📈 Real-Time Sensor Data")
            st.line_chart(st.session_state.data, height=300)

        # --- Логика статуса ---
        msg = f"Temp: {temp:.1f}°C | Vib: {vib:.2f} mm/s"
        if prediction == -1 or risk_index > 70:
            status_box.error(f"🚨 CRITICAL | {msg}")
        elif risk_index > 40:
            status_box.warning(f"⚠️ WARNING | {msg}")
        else:
            status_box.success(f"✅ NORMAL | {msg}")

        # Fusion Risk Index
        fusion_box.metric("Fusion Risk Index", f"{risk_index} / 100")

        # Прогресс
        progress_bar.progress((cycle + 1) / 50)
        st.session_state.cycle = cycle

        time.sleep(0.5)

# --- SIDEBAR ---
st.sidebar.header("System Info")
st.sidebar.write("**Thermal DNA Fusion + AI** - Predictive maintenance for FPSO")
st.sidebar.write("**Sensors:** 8 thermal + 4 vibration")
st.sidebar.write("**Sampling:** 1 Hz")
st.sidebar.write("**AI Model:** Isolation Forest (real-time anomaly detection)")

st.markdown("---")
st.caption("Thermal DNA Fusion Simulator v3.0 | AVCS DNA + AI Monitoring System")
