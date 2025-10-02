# thermal_dna_app.py - AVCS DNA Industrial Monitor v4.1
import streamlit as st
import numpy as np
import pandas as pd
import time
from sklearn.ensemble import IsolationForest

# --- INDUSTRIAL CONFIG ---
st.set_page_config(page_title="AVCS DNA Industrial Monitor", layout="wide")

# --- INDUSTRIAL ARCHITECTURE ---
class IndustrialConfig:
    # Vibration Sensors (ICP piezoelectric)
    VIBRATION_SENSORS = {
        'VIB_MOTOR_DRIVE': 'Motor Drive End',
        'VIB_MOTOR_NONDRIVE': 'Motor Non-Drive End', 
        'VIB_PUMP_INLET': 'Pump Inlet Bearing',
        'VIB_PUMP_OUTLET': 'Pump Outlet Bearing'
    }
    
    # MR Dampers (LORD Corporation)
    MR_DAMPERS = {
        'DAMPER_FRONT_LEFT': 'Front-Left (LORD RD-8040)',
        'DAMPER_FRONT_RIGHT': 'Front-Right (LORD RD-8040)',
        'DAMPER_REAR_LEFT': 'Rear-Left (LORD RD-8040)',
        'DAMPER_REAR_RIGHT': 'Rear-Right (LORD RD-8040)'
    }
    
    # Thermal Sensors (FLIR/Omron)
    THERMAL_SENSORS = {
        'TEMP_MOTOR_WINDING': 'Motor Winding',
        'TEMP_MOTOR_BEARING': 'Motor Bearing',
        'TEMP_PUMP_BEARING': 'Pump Bearing',
        'TEMP_PUMP_CASING': 'Pump Casing'
    }
    
    # Industrial Thresholds
    VIBRATION_LIMITS = {'normal': 2.0, 'warning': 4.0, 'critical': 6.0}
    TEMPERATURE_LIMITS = {'normal': 70, 'warning': 85, 'critical': 100}
    DAMPER_FORCES = {'standby': 500, 'normal': 1000, 'warning': 4000, 'critical': 8000}

# --- HEADER ---
st.title("🏭 AVCS DNA - Industrial Monitoring System")
st.markdown("**Active Vibration Control System with AI-Powered Predictive Maintenance**")

# --- INDUSTRIAL STATE INIT ---
if "system_running" not in st.session_state:
    st.session_state.system_running = False
if "vibration_data" not in st.session_state:
    st.session_state.vibration_data = pd.DataFrame(columns=list(IndustrialConfig.VIBRATION_SENSORS.keys()))
if "temperature_data" not in st.session_state:
    st.session_state.temperature_data = pd.DataFrame(columns=list(IndustrialConfig.THERMAL_SENSORS.keys()))
if "damper_forces" not in st.session_state:
    st.session_state.damper_forces = {damper: 0 for damper in IndustrialConfig.MR_DAMPERS.keys()}
if "damper_history" not in st.session_state:
    st.session_state.damper_history = pd.DataFrame(columns=list(IndustrialConfig.MR_DAMPERS.keys()))
if "ai_model" not in st.session_state:
    # Industrial AI training on normal operation data
    normal_vibration = np.random.normal(1.0, 0.3, (500, 4))
    normal_temperature = np.random.normal(65, 5, (500, 4))
    normal_operation_data = np.column_stack([normal_vibration, normal_temperature])
    
    st.session_state.ai_model = IsolationForest(
        contamination=0.08, 
        random_state=42,
        n_estimators=150
    )
    st.session_state.ai_model.fit(normal_operation_data)

# --- INDUSTRIAL CONTROL PANEL ---
st.sidebar.header("🎛️ AVCS DNA Control Panel")

# System Controls
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("⚡ Start System", type="primary", use_container_width=True):
        st.session_state.system_running = True
        st.session_state.vibration_data = pd.DataFrame(columns=list(IndustrialConfig.VIBRATION_SENSORS.keys()))
        st.session_state.temperature_data = pd.DataFrame(columns=list(IndustrialConfig.THERMAL_SENSORS.keys()))
        st.session_state.damper_forces = {damper: IndustrialConfig.DAMPER_FORCES['standby'] for damper in IndustrialConfig.MR_DAMPERS.keys()}
        st.session_state.damper_history = pd.DataFrame(columns=list(IndustrialConfig.MR_DAMPERS.keys()))
        
with col2:
    if st.button("🛑 Emergency Stop", use_container_width=True):
        st.session_state.system_running = False
        st.session_state.damper_forces = {damper: 0 for damper in IndustrialConfig.MR_DAMPERS.keys()}

# System Status
st.sidebar.markdown("---")
st.sidebar.subheader("📊 System Status")
status_indicator = st.sidebar.empty()

# --- INDUSTRIAL DASHBOARD LAYOUT ---

# Вибромониторинг
st.subheader("📈 Vibration Monitoring")
vib_col1, vib_col2 = st.columns([3, 1])

with vib_col1:
    vibration_chart = st.empty()
    
with vib_col2:
    st.write("**Vibration Sensors:**")
    vibration_status = st.empty()

# Термальный мониторинг  
st.subheader("🌡️ Thermal Monitoring")
temp_col1, temp_col2 = st.columns([3, 1])

with temp_col1:
    temperature_chart = st.empty()
    
with temp_col2:
    st.write("**Thermal Sensors:**")
    temperature_status = st.empty()

# ДЕМПФЕРЫ - НОВЫЙ РАЗДЕЛ
st.markdown("---")
st.subheader("🔄 Active MR Dampers Control")

# График демпферов
st.write("**Damper Force Output:**")
damper_chart = st.empty()

# Статус демпферов в реальном времени
st.write("**Real-time Damper Status:**")
damper_cols = st.columns(4)
damper_status_display = st.empty()

# AI анализ
st.subheader("🤖 AI Fusion Analysis")
fusion_col1, fusion_col2, fusion_col3 = st.columns([2, 1, 1])

with fusion_col1:
    fusion_chart = st.empty()
    
with fusion_col2:
    risk_indicator = st.empty()
    
with fusion_col3:
    ai_confidence = st.empty()

# --- INDUSTRIAL MAIN LOOP ---
if st.session_state.system_running:
    progress_bar = st.sidebar.progress(0)
    cycle_counter = st.sidebar.empty()
    
    for cycle in range(100):
        if not st.session_state.system_running:
            break

        # Генерация данных
        if cycle < 30:
            vibration_readings = {
                'VIB_MOTOR_DRIVE': 1.2 + np.random.normal(0, 0.2),
                'VIB_MOTOR_NONDRIVE': 1.1 + np.random.normal(0, 0.15),
                'VIB_PUMP_INLET': 0.9 + np.random.normal(0, 0.1),
                'VIB_PUMP_OUTLET': 1.0 + np.random.normal(0, 0.12)
            }
            temperature_readings = {
                'TEMP_MOTOR_WINDING': 65 + np.random.normal(0, 3),
                'TEMP_MOTOR_BEARING': 68 + np.random.normal(0, 2),
                'TEMP_PUMP_BEARING': 62 + np.random.normal(0, 2),
                'TEMP_PUMP_CASING': 60 + np.random.normal(0, 1)
            }
        elif cycle < 60:
            degradation = (cycle - 30) * 0.05
            vibration_readings = {
                'VIB_MOTOR_DRIVE': 1.2 + degradation + np.random.normal(0, 0.3),
                'VIB_MOTOR_NONDRIVE': 1.1 + degradation * 0.8 + np.random.normal(0, 0.25),
                'VIB_PUMP_INLET': 0.9 + degradation * 0.6 + np.random.normal(0, 0.15),
                'VIB_PUMP_OUTLET': 1.0 + degradation * 0.7 + np.random.normal(0, 0.18)
            }
            temperature_readings = {
                'TEMP_MOTOR_WINDING': 65 + degradation * 2 + np.random.normal(0, 4),
                'TEMP_MOTOR_BEARING': 68 + degradation * 3 + np.random.normal(0, 3),
                'TEMP_PUMP_BEARING': 62 + degradation * 1.5 + np.random.normal(0, 2),
                'TEMP_PUMP_CASING': 60 + degradation * 1 + np.random.normal(0, 1.5)
            }
        else:
            vibration_readings = {
                'VIB_MOTOR_DRIVE': 5.5 + np.random.normal(0, 0.5),
                'VIB_MOTOR_NONDRIVE': 4.8 + np.random.normal(0, 0.4),
                'VIB_PUMP_INLET': 3.2 + np.random.normal(0, 0.3),
                'VIB_PUMP_OUTLET': 3.8 + np.random.normal(0, 0.35)
            }
            temperature_readings = {
                'TEMP_MOTOR_WINDING': 95 + np.random.normal(0, 5),
                'TEMP_MOTOR_BEARING': 102 + np.random.normal(0, 4),
                'TEMP_PUMP_BEARING': 88 + np.random.normal(0, 3),
                'TEMP_PUMP_CASING': 82 + np.random.normal(0, 2)
            }

        # Сохраняем данные
        st.session_state.vibration_data.loc[cycle] = vibration_readings
        st.session_state.temperature_data.loc[cycle] = temperature_readings

        # AI анализ
        vibration_features = list(vibration_readings.values())
        temperature_features = list(temperature_readings.values())
        industrial_features = np.array([vibration_features + temperature_features])
        
        ai_prediction = st.session_state.ai_model.predict(industrial_features)[0]
        ai_confidence_score = st.session_state.ai_model.decision_function(industrial_features)[0]
        
        risk_index = min(100, max(0, int((abs(ai_confidence_score) * 120))))
        
        # УПРАВЛЕНИЕ ДЕМПФЕРАМИ
        max_vibration = max(vibration_readings.values())
        max_temperature = max(temperature_readings.values())
        
        if ai_prediction == -1 or risk_index > 80:
            damper_force = IndustrialConfig.DAMPER_FORCES['critical']
            system_status = "🚨 CRITICAL"
            status_color = "red"
            damper_status = "MAX FORCE"
        elif risk_index > 50:
            damper_force = IndustrialConfig.DAMPER_FORCES['warning'] 
            system_status = "⚠️ WARNING"
            status_color = "orange"
            damper_status = "HIGH FORCE"
        elif risk_index > 20:
            damper_force = IndustrialConfig.DAMPER_FORCES['normal']
            system_status = "✅ NORMAL" 
            status_color = "green"
            damper_status = "NORMAL FORCE"
        else:
            damper_force = IndustrialConfig.DAMPER_FORCES['standby']
            system_status = "🟢 STANDBY"
            status_color = "blue"
            damper_status = "STANDBY"
        
        # Применяем силу ко всем демпферам
        st.session_state.damper_forces = {damper: damper_force for damper in IndustrialConfig.MR_DAMPERS.keys()}
        st.session_state.damper_history.loc[cycle] = st.session_state.damper_forces

        # ОБНОВЛЕНИЕ ИНТЕРФЕЙСА
        
        # Вибрография
        with vibration_chart:
            st.line_chart(st.session_state.vibration_data, height=200)
        
        # Статус вибродатчиков
        with vibration_status:
            for sensor, value in vibration_readings.items():
                location = IndustrialConfig.VIBRATION_SENSORS[sensor]
                status = "Normal" if value < 2.0 else "Warning" if value < 4.0 else "Critical"
                color = "🟢" if value < 2.0 else "🟡" if value < 4.0 else "🔴"
                st.write(f"{color} {location}: {value:.1f} mm/s")
        
        # Термография
        with temperature_chart:
            st.line_chart(st.session_state.temperature_data, height=200)
        
        # Статус термодатчиков
        with temperature_status:
            for sensor, value in temperature_readings.items():
                location = IndustrialConfig.THERMAL_SENSORS[sensor]
                status = "Normal" if value < 70 else "Warning" if value < 85 else "Critical"
                color = "🟢" if value < 70 else "🟡" if value < 85 else "🔴"
                st.write(f"{color} {location}: {value:.0f}°C")
        
        # ГРАФИК ДЕМПФЕРОВ
        with damper_chart:
            if len(st.session_state.damper_history) > 0:
                st.line_chart(st.session_state.damper_history, height=200)
        
        # СТАТУС ДЕМПФЕРОВ В РЕАЛЬНОМ ВРЕМЕНИ
        with damper_status_display:
            damper_cols = st.columns(4)
            for i, (damper, location) in enumerate(IndustrialConfig.MR_DAMPERS.items()):
                with damper_cols[i]:
                    force = st.session_state.damper_forces[damper]
                    if force >= 4000:
                        st.error(f"🔴 {location}\n{force} N\nMAX FORCE")
                    elif force >= 1000:
                        st.warning(f"🟡 {location}\n{force} N\nACTIVE")
                    else:
                        st.success(f"🟢 {location}\n{force} N\nSTANDBY")
        
        # AI анализ
        with fusion_col1:
            fusion_data = pd.DataFrame({
                'Vibration Risk': [max_vibration * 15],
                'Temperature Risk': [max_temperature],
                'AI Confidence': [abs(ai_confidence_score) * 50]
            })
            st.line_chart(fusion_data, height=150)
        
        with fusion_col2:
            risk_indicator.metric("🔴 Risk Index", f"{risk_index}/100")
            
        with fusion_col3:
            ai_confidence.metric("🤖 AI Confidence", f"{abs(ai_confidence_score):.2f}")
        
        # Системный статус
        status_indicator.markdown(f"<h3 style='color: {status_color};'>{system_status} | Dampers: {damper_status}</h3>", unsafe_allow_html=True)
        
        # Прогресс
        progress_bar.progress((cycle + 1) / 100)
        cycle_counter.text(f"🔄 Cycle: {cycle + 1}/100")
        
        time.sleep(0.3)

# Документация
st.sidebar.markdown("---")
st.sidebar.subheader("🏭 System Architecture")
st.sidebar.write("**Vibration Sensors:** 4x PCB 603C01")
st.sidebar.write("**MR Dampers:** 4x LORD RD-8040-01") 
st.sidebar.write("**Thermal Sensors:** 4x FLIR A500f")
st.sidebar.write("**Controller:** Beckhoff CX2040")

st.sidebar.markdown("---")
st.sidebar.subheader("💰 Business Value")
st.sidebar.metric("System Cost", "$250,000")
st.sidebar.metric("ROI", ">2000%")

st.markdown("---")
st.caption("AVCS DNA Industrial Monitor v4.1 | Yeruslan Technologies")
