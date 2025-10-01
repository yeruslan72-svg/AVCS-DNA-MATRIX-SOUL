import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime

st.set_page_config(page_title="Thermal DNA Simulator", layout="wide")

# ---------------- CONFIG ----------------
BUFFER_SIZE = 50
TEMP_NORMAL = (40, 60)     # рабочая зона
TEMP_WARNING = (61, 80)    # тревога
TEMP_CRITICAL = (81, 120)  # критично

# ---------------- STATE ----------------
if "temps" not in st.session_state:
    st.session_state.temps = []
if "running" not in st.session_state:
    st.session_state.running = False

# ---------------- FUNCTIONS ----------------
def generate_temperature(cycle: int) -> float:
    """Симуляция тепловых данных"""
    if cycle < 20:
        return np.random.normal(55, 2)  # нормальная работа
    elif cycle < 40:
        return np.random.normal(72, 3)  # перегрев
    else:
        return np.random.normal(95, 4)  # критично

def analyze_temperature(temp: float) -> str:
    """Анализ состояния"""
    if TEMP_NORMAL[0] <= temp <= TEMP_NORMAL[1]:
        return "✅ NORMAL"
    elif TEMP_WARNING[0] <= temp <= TEMP_WARNING[1]:
        return "⚠️ WARNING"
    else:
        return "🚨 CRITICAL"

# ---------------- UI ----------------
st.title("🌡️ Thermal DNA Simulator")
st.markdown("**Fusion demo:** real-time monitoring of thermal anomalies (AVCS DNA)")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Temperature over time")
    chart = st.empty()

with col2:
    st.subheader("Current status")
    status_box = st.empty()
    action_box = st.empty()

start_button = st.button("▶️ Start Simulation")
stop_button = st.button("⏹ Stop Simulation")

if start_button:
    st.session_state.running = True
    st.session_state.temps = []

if stop_button:
    st.session_state.running = False

# ---------------- LOOP ----------------
if st.session_state.running:
    for cycle in range(60):
        temp = generate_temperature(cycle)
        st.session_state.temps.append(temp)

        status = analyze_temperature(temp)

        # Рисуем график
        fig, ax = plt.subplots()
        ax.plot(st.session_state.temps, color="red", marker="o")
        ax.set_ylim(30, 120)
        ax.set_ylabel("Temperature (°C)")
        ax.set_xlabel("Cycle")
        ax.axhspan(*TEMP_NORMAL, color="green", alpha=0.1, label="Normal")
        ax.axhspan(*TEMP_WARNING, color="orange", alpha=0.1, label="Warning")
        ax.axhspan(*TEMP_CRITICAL, color="red", alpha=0.1, label="Critical")
        ax.legend(loc="upper left")
        chart.pyplot(fig)

        # Текущий статус
        status_box.markdown(f"### {status}")
        if "CRITICAL" in status:
            action_box.error("IMMEDIATE MAINTENANCE REQUIRED!")
        elif "WARNING" in status:
            action_box.warning("Monitor closely.")
        else:
            action_box.success("System operating normally.")

        time.sleep(0.5)
