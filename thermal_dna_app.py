# thermal_dna_app.py - Thermal DNA Simulator (improved visualization)
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Thermal DNA", layout="wide")

# ---------------- CONFIG ----------------
st.title("🌡️ Thermal DNA Simulator")
st.markdown("**Real-time thermal monitoring for FPSO equipment (AVCS DNA)**")

if "running" not in st.session_state:
    st.session_state.running = False
if "temps" not in st.session_state:
    st.session_state.temps = []
if "cycle" not in st.session_state:
    st.session_state.cycle = 0

# ---------------- CONTROL PANEL ----------------
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start Simulation", type="primary"):
        st.session_state.running = True
        st.session_state.temps = []
        st.session_state.cycle = 0
        
with col2:
    if st.button("⏹️ Stop Simulation"):
        st.session_state.running = False

# ---------------- MAIN LOOP ----------------
if st.session_state.running:
    placeholder = st.empty()
    
    for cycle in range(50):
        if not st.session_state.running:
            break
            
        # Симуляция температуры (3 этапа: норм, перегрев, критика)
        if cycle < 20:
            temp = 55 + np.random.normal(0, 2)
        elif cycle < 40:
            temp = 70 + np.random.normal(0, 3)
        else:
            temp = 90 + np.random.normal(0, 4)
            
        st.session_state.temps.append(temp)
        st.session_state.cycle = cycle
        
        # -------- Визуализация --------
        with placeholder.container():
            fig, ax = plt.subplots(figsize=(10, 4))
            temps = st.session_state.temps
            
            # Линия температуры
            ax.plot(temps, 'r-', linewidth=2, marker='o', label="Temperature")
            
            # Подсветка текущей точки
            ax.scatter(len(temps)-1, temps[-1], color='blue', s=100, zorder=5, label="Current")
            
            # Зоны риска
            ax.axhspan(40, 60, color='green', alpha=0.2, label='Normal')
            ax.axhspan(61, 80, color='orange', alpha=0.2, label='Warning')
            ax.axhspan(81, 120, color='red', alpha=0.2, label='Critical')
            
            ax.set_ylim(40, 120)
            ax.set_xlabel("Cycle")
            ax.set_ylabel("Temperature (°C)")
            ax.set_title(f"Thermal DNA Monitoring - Cycle {cycle}")
            ax.legend(loc="upper left")
            
            st.pyplot(fig)
            
            # -------- Статус --------
            if temp > 80:
                st.error(f"🚨 CRITICAL: {temp:.1f}°C - Immediate maintenance required!")
            elif temp > 60:
                st.warning(f"⚠️ WARNING: {temp:.1f}°C - Monitor closely")
            else:
                st.success(f"✅ NORMAL: {temp:.1f}°C")
                
            # Прогресс симуляции
            st.progress((cycle + 1) / 50)
        
        time.sleep(0.5)  # пауза для реалистичности

# ---------------- SIDEBAR ----------------
st.sidebar.header("System Info")
st.sidebar.write("**Thermal DNA** - Predictive maintenance")
st.sidebar.write("**Sensors:** 8 thermal sensors")
st.sidebar.write("**Sampling:** 1 Hz")
st.sidebar.write("**AI Analysis:** Real-time anomaly detection")

st.markdown("---")
st.caption("Thermal DNA Simulator v1.1 | AVCS DNA Fusion System")

