# streamlit_app.py - AVCS DNA Industrial Monitor (WITH CHARTS)
import streamlit as st
import numpy as np
import pandas as pd
import time

# УБИРАЕМ set_page_config полностью
# st.set_page_config(page_title="AVCS DNA Monitor", layout="wide")

st.title("🏭 AVCS DNA Industrial Monitor")
st.write("AI-Powered Predictive Maintenance System")

# Инициализация состояния с DataFrame
if "system_running" not in st.session_state:
    st.session_state.system_running = False
if "vibration_data" not in st.session_state:
    st.session_state.vibration_data = pd.DataFrame(columns=['Motor Drive', 'Motor Non-Drive', 'Pump Inlet', 'Pump Outlet'])
if "temperature_data" not in st.session_state:
    st.session_state.temperature_data = pd.DataFrame(columns=['Motor Winding', 'Motor Bearing', 'Pump Bearing', 'Pump Casing'])
if "current_cycle" not in st.session_state:
    st.session_state.current_cycle = 0

# Панель управления
st.sidebar.header("Control Panel")

if st.sidebar.button("⚡ Start Monitoring"):
    st.session_state.system_running = True
    st.session_state.vibration_data = pd.DataFrame(columns=['Motor Drive', 'Motor Non-Drive', 'Pump Inlet', 'Pump Outlet'])
    st.session_state.temperature_data = pd.DataFrame(columns=['Motor Winding', 'Motor Bearing', 'Pump Bearing', 'Pump Casing'])
    st.session_state.current_cycle = 0
    st.rerun()

if st.sidebar.button("🛑 Stop Monitoring"):
    st.session_state.system_running = False
    st.rerun()

# Основное приложение
if not st.session_state.system_running:
    st.info("Click 'Start Monitoring' to begin real-time monitoring")
else:
    # Генерация данных для 4 сенсоров
    cycle = st.session_state.current_cycle
    
    if cycle < 30:
        # Нормальная работа
        base_vib = 1.0
        base_temp = 65
        status = "🟢 NORMAL"
    elif cycle < 60:
        # Предупреждение
        base_vib = 3.0
        base_temp = 75
        status = "🟡 WARNING"
    else:
        # Критическое состояние
        base_vib = 6.0
        base_temp = 90
        status = "🔴 CRITICAL"
    
    # Данные для 4 вибро-сенсоров
    vibration_data = {
        'Motor Drive': max(0.1, base_vib + np.random.normal(0, 0.2)),
        'Motor Non-Drive': max(0.1, base_vib + np.random.normal(0, 0.3)),
        'Pump Inlet': max(0.1, base_vib + np.random.normal(0, 0.25)),
        'Pump Outlet': max(0.1, base_vib + np.random.normal(0, 0.35))
    }
    
    # Данные для 4 температурных сенсоров
    temperature_data = {
        'Motor Winding': max(20, base_temp + np.random.normal(0, 3)),
        'Motor Bearing': max(20, base_temp + np.random.normal(0, 4)),
        'Pump Bearing': max(20, base_temp + np.random.normal(0, 5)),
        'Pump Casing': max(20, base_temp + np.random.normal(0, 2))
    }
    
    # Добавляем данные в DataFrame
    st.session_state.vibration_data = pd.concat([
        st.session_state.vibration_data, 
        pd.DataFrame([vibration_data])
    ], ignore_index=True)
    
    st.session_state.temperature_data = pd.concat([
        st.session_state.temperature_data,
        pd.DataFrame([temperature_data])
    ], ignore_index=True)
    
    # Ограничиваем историю (последние 50 точек)
    if len(st.session_state.vibration_data) > 50:
        st.session_state.vibration_data = st.session_state.vibration_data.iloc[1:]
    if len(st.session_state.temperature_data) > 50:
        st.session_state.temperature_data = st.session_state.temperature_data.iloc[1:]
    
    # ОТОБРАЖЕНИЕ ГРАФИКОВ
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Vibration Sensors")
        if not st.session_state.vibration_data.empty:
            st.line_chart(st.session_state.vibration_data, height=300)
        
        # Текущие значения вибрации
        st.write("**Current Vibration Values:**")
        for sensor, value in vibration_data.items():
            st.write(f"{sensor}: {value:.2f} mm/s")
    
    with col2:
        st.subheader("🌡️ Temperature Sensors")
        if not st.session_state.temperature_data.empty:
            st.line_chart(st.session_state.temperature_data, height=300)
        
        # Текущие значения температуры
        st.write("**Current Temperature Values:**")
        for sensor, value in temperature_data.items():
            st.write(f"{sensor}: {value:.1f} °C")
    
    # Статус системы
    st.subheader("🚨 System Status")
    if status == "🔴 CRITICAL":
        st.error(f"{status} - Immediate maintenance required!")
    elif status == "🟡 WARNING":
        st.warning(f"{status} - Monitor equipment closely")
    else:
        st.success(f"{status} - Operating normally")
    
    # Прогресс и информация
    st.sidebar.write(f"**Cycle:** {st.session_state.current_cycle}/100")
    progress = st.session_state.current_cycle / 100
    st.sidebar.progress(progress)
    
    # Следующий цикл
    st.session_state.current_cycle += 1
    
    if st.session_state.current_cycle >= 100:
        st.balloons()
        st.success("✅ Monitoring session completed successfully!")
        st.session_state.system_running = False
    else:
        time.sleep(1)
        st.rerun()

st.write("---")
st.caption("AVCS DNA Matrix Soul v6.0 | Yeruslan Technologies | Predictive Maintenance System")
