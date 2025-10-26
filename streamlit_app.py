# streamlit_app.py - AVCS DNA with PLOTLY CHARTS
import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.graph_objects as go
import plotly.express as px

st.title("🏭 AVCS DNA Industrial Monitor")
st.write("AI-Powered Predictive Maintenance System")

# Инициализация
if "system_running" not in st.session_state:
    st.session_state.system_running = False
if "vibration_data" not in st.session_state:
    st.session_state.vibration_data = pd.DataFrame(columns=['Motor_Drive', 'Motor_NonDrive', 'Pump_Inlet', 'Pump_Outlet'])
if "temperature_data" not in st.session_state:
    st.session_state.temperature_data = pd.DataFrame(columns=['Motor_Winding', 'Motor_Bearing', 'Pump_Bearing', 'Pump_Casing'])
if "current_cycle" not in st.session_state:
    st.session_state.current_cycle = 0

# Управление
st.sidebar.header("Control Panel")
if st.sidebar.button("⚡ Start Monitoring"):
    st.session_state.system_running = True
    st.session_state.vibration_data = pd.DataFrame(columns=['Motor_Drive', 'Motor_NonDrive', 'Pump_Inlet', 'Pump_Outlet'])
    st.session_state.temperature_data = pd.DataFrame(columns=['Motor_Winding', 'Motor_Bearing', 'Pump_Bearing', 'Pump_Casing'])
    st.session_state.current_cycle = 0
    st.rerun()

if st.sidebar.button("🛑 Stop Monitoring"):
    st.session_state.system_running = False
    st.rerun()

if not st.session_state.system_running:
    st.info("Click 'Start Monitoring' to begin real-time monitoring")
else:
    # Генерация данных
    cycle = st.session_state.current_cycle
    
    if cycle < 30:
        base_vib, base_temp, status = 1.0, 65, "🟢 NORMAL"
    elif cycle < 60:
        base_vib, base_temp, status = 3.0, 75, "🟡 WARNING"
    else:
        base_vib, base_temp, status = 6.0, 90, "🔴 CRITICAL"
    
    # Новые данные
    new_vibration = {
        'Motor_Drive': max(0.1, base_vib + np.random.normal(0, 0.2)),
        'Motor_NonDrive': max(0.1, base_vib + np.random.normal(0, 0.3)),
        'Pump_Inlet': max(0.1, base_vib + np.random.normal(0, 0.25)),
        'Pump_Outlet': max(0.1, base_vib + np.random.normal(0, 0.35))
    }
    
    new_temperature = {
        'Motor_Winding': max(20, base_temp + np.random.normal(0, 3)),
        'Motor_Bearing': max(20, base_temp + np.random.normal(0, 4)),
        'Pump_Bearing': max(20, base_temp + np.random.normal(0, 5)),
        'Pump_Casing': max(20, base_temp + np.random.normal(0, 2))
    }
    
    # Добавляем данные
    st.session_state.vibration_data = pd.concat([
        st.session_state.vibration_data, 
        pd.DataFrame([new_vibration])
    ], ignore_index=True)
    
    st.session_state.temperature_data = pd.concat([
        st.session_state.temperature_data,
        pd.DataFrame([new_temperature])
    ], ignore_index=True)
    
    # Ограничиваем историю
    if len(st.session_state.vibration_data) > 40:
        st.session_state.vibration_data = st.session_state.vibration_data.iloc[1:]
    if len(st.session_state.temperature_data) > 40:
        st.session_state.temperature_data = st.session_state.temperature_data.iloc[1:]
    
    # ОТОБРАЖЕНИЕ С PLOTLY
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Vibration Sensors")
        if not st.session_state.vibration_data.empty:
            # Создаем Plotly график для вибрации
            fig_vib = go.Figure()
            for column in st.session_state.vibration_data.columns:
                fig_vib.add_trace(go.Scatter(
                    y=st.session_state.vibration_data[column],
                    name=column.replace('_', ' '),
                    mode='lines'
                ))
            fig_vib.update_layout(
                title="Vibration Monitoring",
                xaxis_title="Time",
                yaxis_title="Vibration (mm/s)",
                height=300
            )
            st.plotly_chart(fig_vib, use_container_width=True)
        
        # Текущие значения
        st.write("**Current Values:**")
        for sensor, value in new_vibration.items():
            st.write(f"• {sensor.replace('_', ' ')}: {value:.2f} mm/s")
    
    with col2:
        st.subheader("🌡️ Temperature Sensors")
        if not st.session_state.temperature_data.empty:
            # Создаем Plotly график для температуры
            fig_temp = go.Figure()
            for column in st.session_state.temperature_data.columns:
                fig_temp.add_trace(go.Scatter(
                    y=st.session_state.temperature_data[column],
                    name=column.replace('_', ' '),
                    mode='lines'
                ))
            fig_temp.update_layout(
                title="Temperature Monitoring",
                xaxis_title="Time", 
                yaxis_title="Temperature (°C)",
                height=300
            )
            st.plotly_chart(fig_temp, use_container_width=True)
        
        # Текущие значения
        st.write("**Current Values:**")
        for sensor, value in new_temperature.items():
            st.write(f"• {sensor.replace('_', ' ')}: {value:.1f} °C")
    
    # Статус
    st.subheader("🚨 System Status")
    if status == "🔴 CRITICAL":
        st.error(f"{status} - Immediate maintenance required!")
    elif status == "🟡 WARNING":
        st.warning(f"{status} - Monitor equipment closely")
    else:
        st.success(f"{status} - Operating normally")
    
    # Прогресс
    st.sidebar.write(f"**Cycle:** {st.session_state.current_cycle}/100")
    st.sidebar.progress(st.session_state.current_cycle / 100)
    
    # Следующий цикл
    st.session_state.current_cycle += 1
    
    if st.session_state.current_cycle >= 100:
        st.balloons()
        st.success("✅ Monitoring completed!")
        st.session_state.system_running = False
    else:
        time.sleep(1)
        st.rerun()

st.write("---")
st.caption("AVCS DNA Matrix Soul v6.0 | Yeruslan Technologies")
