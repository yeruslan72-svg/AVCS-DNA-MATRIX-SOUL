import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest
import random
import time

# ================================
# ⚡ AVCS DNA Thermal Simulator v5.2
# ================================

st.set_page_config(page_title="Thermal DNA Simulator v5.2", layout="wide")

st.title("🌡️ Thermal DNA Simulator v5.2 | AVCS DNA Fusion System")
st.markdown("Real-time monitoring & AI risk prediction for FPSO equipment")

# --- Sidebar ---
st.sidebar.header("⚙️ Simulation Controls")
sim_speed = st.sidebar.slider("Simulation Speed (sec/update)", 0.1, 2.0, 0.5)
add_noise = st.sidebar.checkbox("Add Random Noise", True)

# --- Initialize session state ---
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["time", "temp", "vib", "noise", "risk"])

# --- Generate fake sensor data ---
def generate_data(tick):
    base_temp = 55 + 0.02 * tick
    base_vib = 1.2 + 0.005 * tick
    base_noise = 65 + 0.03 * tick  # acoustic level in dB
    
    if add_noise:
        temp = base_temp + np.random.normal(0, 0.5)
        vib = base_vib + np.random.normal(0, 0.1)
        noise = base_noise + np.random.normal(0, 1.0)
    else:
        temp, vib, noise = base_temp, base_vib, base_noise
    
    return temp, vib, noise

# --- AI Model (Isolation Forest) ---
def ai_predict(df):
    if len(df) < 20:
        return 0, "Learning..."
    
    model = IsolationForest(contamination=0.1, random_state=42)
    features = df[["temp", "vib", "noise"]]
    preds = model.fit_predict(features)
    anomaly_score = list(preds)[-1]
    
    risk_index = np.clip(
        0.4 * (df["temp"].iloc[-1] - 50) +
        0.4 * (df["vib"].iloc[-1] * 15) +
        0.2 * (df["noise"].iloc[-1] - 60),
        0, 100
    )
    
    status = "🟢 NORMAL"
    if risk_index > 80:
        status = "🔴 CRITICAL"
    elif risk_index > 50:
        status = "🟡 WARNING"
    
    return risk_index, status

# --- Remaining Useful Life (RUL) estimation ---
def estimate_rul(df):
    if len(df) < 10:
        return "Collecting data..."
    
    temp_trend = np.polyfit(range(len(df)), df["temp"], 1)[0]
    vib_trend = np.polyfit(range(len(df)), df["vib"], 1)[0]
    
    hours_left_temp = (80 - df["temp"].iloc[-1]) / temp_trend if temp_trend > 0 else np.inf
    hours_left_vib = (3.5 - df["vib"].iloc[-1]) / vib_trend if vib_trend > 0 else np.inf
    
    hours_left = min(hours_left_temp, hours_left_vib)
    if hours_left == np.inf:
        return "Stable"
    return f"~{int(hours_left)} ticks to failure"

# --- Main Simulation Loop ---
tick = len(st.session_state.data)
temp, vib, noise = generate_data(tick)

new_row = {"time": tick, "temp": temp, "vib": vib, "noise": noise, "risk": 0}
st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)

risk_index, system_status = ai_predict(st.session_state.data)
st.session_state.data.at[tick, "risk"] = risk_index
rul_estimate = estimate_rul(st.session_state.data)

# --- Layout ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Sensor Readings Over Time")
    st.line_chart(st.session_state.data.set_index("time")[["temp", "vib", "noise"]])

with col2:
    st.subheader("🤖 AI Fusion Analysis")
    st.metric("System Status", system_status)
    st.metric("Estimated RUL", rul_estimate)
    
    # 🎯 Gauge Indicator for Risk
    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_index,
        title={'text': "Risk Index"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "green"},
                {'range': [50, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': risk_index
            }
        }
    ))
    st.plotly_chart(gauge_fig, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.caption("AVCS DNA Fusion System v5.2 | Powered by Thermal DNA AI Core")

# Auto-refresh
time.sleep(sim_speed)
st.experimental_rerun()
