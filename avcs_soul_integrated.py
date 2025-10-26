# avcs_soul_integrated.py - ПОЛНАЯ ИНТЕГРИРОВАННАЯ СИСТЕМА
import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import sys
import os

# Добавляем пути к модулям
sys.path.append('digital_twin')
sys.path.append('plc_integration') 
sys.path.append('voice_system')

# --- ИМПОРТ ВСЕХ МОДУЛЕЙ ---
try:
    # Digital Twin модуль
    from digital_twins import IndustrialDigitalTwin
    
    # PLC Integration модуль  
    from system_integrator import create_soul_integrator
    from industrial_plc import create_avcs_plc_integration
    
    # Voice System модуль
    from voice_interface import create_voice_interface
    from english_voice_soul import create_english_voice_personality
    from emotional_display import create_emotional_display
    
    MODULES_LOADED = True
except ImportError as e:
    print(f"Module import warning: {e}")
    MODULES_LOADED = False
    # Заглушки для разработки
    class IndustrialDigitalTwin:
        def __init__(self, equipment_type="centrifugal_pump"):
            self.equipment_type = equipment_type
            self.operational_data = {}
        
        def simulate_equipment_behavior(self, operating_conditions):
            return {
                'vibration_data': np.random.normal(2.0, 0.5, 100),
                'thermal_data': np.random.normal(70, 5),
                'acoustic_data': np.random.normal(75, 3)
            }
    
    def create_soul_integrator():
        class SoulIntegrator:
            def connect_industrial_bus(self):
                return {"status": "connected", "protocol": "OPC_UA"}
        return SoulIntegrator()
    
    def create_voice_interface():
        class VoiceInterface:
            def render_voice_control_panel(self, personality):
                st.sidebar.info("🎤 Voice System: Simulation Mode")
        return VoiceInterface()
    
    def create_english_voice_personality():
        class VoicePersonality:
            def speak(self, text, emotion):
                print(f"🔊 VOICE [{emotion}]: {text}")
        return VoicePersonality()

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

# --- INTEGRATED SYSTEM MANAGER ---
class AVCSSoulSystem:
    def __init__(self):
        self.modules_loaded = MODULES_LOADED
        self.initialize_modules()
        
    def initialize_modules(self):
        """Инициализация всех модулей системы"""
        try:
            # 1. Digital Twin
            self.digital_twin = IndustrialDigitalTwin("centrifugal_pump")
            print("✅ Digital Twin initialized")
        except Exception as e:
            print(f"❌ Digital Twin failed: {e}")
            self.digital_twin = None
            
        try:
            # 2. PLC Integration
            self.plc_integrator = create_soul_integrator()
            print("✅ PLC Integrator initialized")
        except Exception as e:
            print(f"❌ PLC Integrator failed: {e}")
            self.plc_integrator = None
            
        try:
            # 3. Voice System
            self.voice_personality = create_english_voice_personality()
            self.voice_interface = create_voice_interface()
            print("✅ Voice System initialized")
        except Exception as e:
            print(f"❌ Voice System failed: {e}")
            self.voice_personality = None
            self.voice_interface = None
            
        # Business Intelligence
        self.performance_metrics = {
            'prevented_failures': 0,
            'operational_hours': 0,
            'emergency_stops': 0,
            'total_cycles': 0
        }
        
    def generate_integrated_sensor_data(self, cycle, failure_mode):
        """Генерация данных с использованием Digital Twin"""
        mode_data = FAILURE_MODES[failure_mode]
        
        # Используем Digital Twin если доступен
        if self.digital_twin:
            try:
                operating_conditions = {
                    'rpm': 2950,
                    'load': 'normal', 
                    'ambient_temperature': 25,
                    'failure_mode': failure_mode,
                    'operational_hours': cycle * 0.1
                }
                
                twin_data = self.digital_twin.simulate_equipment_behavior(operating_conditions)
                
                # Извлекаем данные из digital twin
                vibration = {}
                for i, sensor in enumerate(IndustrialConfig.VIBRATION_SENSORS.keys()):
                    if 'vibration_data' in twin_data:
                        base_value = np.mean(twin_data['vibration_data']) if isinstance(twin_data['vibration_data'], (list, np.ndarray)) else 1.0
                        vibration[sensor] = max(0.1, base_value * (1 + i * 0.1))
                    else:
                        vibration[sensor] = max(0.1, mode_data["vib"] + np.random.normal(0, 0.2))
                
                temperature = {}
                for sensor in IndustrialConfig.THERMAL_SENSORS.keys():
                    if 'thermal_data' in twin_data:
                        temp_value = twin_data['thermal_data'] if isinstance(twin_data['thermal_data'], (int, float)) else 65
                        temperature[sensor] = max(20, temp_value + np.random.normal(0, 2))
                    else:
                        temperature[sensor] = max(20, mode_data["temp"] + np.random.normal(0, 2))
                
                noise = twin_data.get('acoustic_data', mode_data["noise"]) if 'acoustic_data' in twin_data else mode_data["noise"]
                noise = max(30, noise + np.random.normal(0, 2))
                
                return vibration, temperature, noise, "Digital Twin Simulation"
                
            except Exception as e:
                print(f"Digital Twin simulation error: {e}")
        
        # Fallback: базовая генерация данных
        vibration = {}
        for i, sensor in enumerate(IndustrialConfig.VIBRATION_SENSORS.keys()):
            vibration[sensor] = max(0.1, mode_data["vib"] + np.random.normal(0, 0.2 + i * 0.1))
        
        temperature = {}
        for sensor in IndustrialConfig.THERMAL_SENSORS.keys():
            temperature[sensor] = max(20, mode_data["temp"] + np.random.normal(0, 2))
        
        noise = max(30, mode_data["noise"] + np.random.normal(0, 2))
        
        return vibration, temperature, noise, "Basic Simulation"
    
    def voice_announcement(self, risk, mode, prevented_failures, rul_hours):
        """Голосовые уведомления через integrated voice system"""
        if self.voice_personality:
            try:
                if risk > 85:
                    self.voice_personality.speak(
                        f"Critical alert! Risk level {risk} percent. Immediate attention required!",
                        "URGENT"
                    )
                elif risk > 60:
                    self.voice_personality.speak(
                        f"Warning condition. Risk at {risk} percent. {FAILURE_MODES[mode]['name']} active.",
                        "ALERT"
                    )
                elif prevented_failures > 0:
                    self.voice_personality.speak(
                        f"Excellent performance! Prevented {prevented_failures} potential failures.",
                        "PROUD"
                    )
            except Exception as e:
                print(f"Voice announcement error: {e}")

# --- INITIALIZATION ---
def initialize_integrated_system():
    """Инициализация integrated системы"""
    if "soul_system" not in st.session_state:
        st.session_state.soul_system = AVCSSoulSystem()
    
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

# --- CALCULATIONS ---
def calculate_risk(vibration, temperature, noise):
    max_vib = max(vibration.values()) if vibration else 0
    max_temp = max(temperature.values()) if temperature else 0
    
    risk = 0
    if max_vib > 6.0: risk += 60
    elif max_vib > 4.0: risk += 40
    elif max_vib > 2.0: risk += 20
        
    if max_temp > 95: risk += 50
    elif max_temp > 85: risk += 30
    elif max_temp > 75: risk += 15
        
    if noise > 95: risk += 40
    elif noise > 85: risk += 25
    elif noise > 75: risk += 10
        
    return min(100, risk)

def calculate_rul(risk_index, cycle):
    base_rul = 100 - risk_index
    if cycle > 50:
        base_rul -= (cycle - 50) * 0.1
    return max(0, int(base_rul))

def calculate_damper_force(risk_index):
    if risk_index > 80: return IndustrialConfig.DAMPER_FORCES['critical']
    elif risk_index > 50: return IndustrialConfig.DAMPER_FORCES['warning']
    elif risk_index > 20: return IndustrialConfig.DAMPER_FORCES['normal']
    else: return IndustrialConfig.DAMPER_FORCES['standby']

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
    fig.update_layout(title=title, xaxis_title="Time", yaxis_title=y_title, height=250)
    return fig

def create_risk_gauge(risk_index):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_index,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "AI Risk Index"},
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
    st.set_page_config(
        page_title="AVCS DNA MATRIX SOUL - Integrated System",
        layout="wide",
        page_icon="🧠"
    )
    
    initialize_integrated_system()
    soul_system = st.session_state.soul_system
    
    st.title("🧠 AVCS DNA MATRIX SOUL - Integrated System")
    st.markdown("**Unified Industrial AI Platform with Digital Twin, PLC Integration & Voice AI**")
    
    # Sidebar
    st.sidebar.header("🎛️ Integrated Control Panel")
    
    # System Status
    st.sidebar.subheader("🔧 System Modules")
    st.sidebar.write(f"✅ Digital Twin: {'Active' if soul_system.digital_twin else 'Simulation'}")
    st.sidebar.write(f"✅ PLC Integration: {'Active' if soul_system.plc_integrator else 'Simulation'}")
    st.sidebar.write(f"✅ Voice AI: {'Active' if soul_system.voice_personality else 'Simulation'}")
    
    # Failure Mode Selection
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔧 Failure Mode")
    for mode_key, mode_data in FAILURE_MODES.items():
        if st.sidebar.button(mode_data["name"], use_container_width=True, key=f"mode_{mode_key}"):
            st.session_state.current_mode = mode_key
            st.rerun()
    
    st.sidebar.write(f"**Active:** {FAILURE_MODES[st.session_state.current_mode]['name']}")
    
    # Control Buttons
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("⚡ Start SOUL", type="primary", use_container_width=True):
            st.session_state.system_running = True
            reset_system_data()
            st.rerun()
    
    with col2:
        if st.button("🛑 Stop System", use_container_width=True):
            st.session_state.system_running = False
            st.session_state.damper_forces = {damper: 500 for damper in IndustrialConfig.MR_DAMPERS.keys()}
            st.rerun()
    
    # Voice Control
    if soul_system.voice_interface and soul_system.voice_personality:
        st.sidebar.markdown("---")
        st.sidebar.subheader("🎤 Voice Control")
        soul_system.voice_interface.render_voice_control_panel(soul_system.voice_personality)
    
    # Settings
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Settings")
    simulation_speed = st.sidebar.slider("Speed", 0.1, 2.0, 0.5, 0.1)
    max_cycles = st.sidebar.slider("Max Cycles", 50, 500, 200, 50)
    
    # Status Display
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 System Status")
    status_display = st.sidebar.empty()
    cycle_display = st.sidebar.empty()
    progress_display = st.sidebar.empty()
    
    # Main Display
    if not st.session_state.system_running:
        show_landing_page(soul_system)
    else:
        run_integrated_monitoring(soul_system, status_display, cycle_display, progress_display, simulation_speed, max_cycles)

def reset_system_data():
    """Сброс данных системы"""
    st.session_state.vibration_data = pd.DataFrame(columns=list(IndustrialConfig.VIBRATION_SENSORS.keys()))
    st.session_state.temperature_data = pd.DataFrame(columns=list(IndustrialConfig.THERMAL_SENSORS.keys()))
    st.session_state.noise_data = pd.DataFrame(columns=['NOISE'])
    st.session_state.damper_data = pd.DataFrame(columns=list(IndustrialConfig.MR_DAMPERS.keys()))
    st.session_state.risk_history = []
    st.session_state.current_cycle = 0
    st.session_state.soul_system.performance_metrics = {
        'prevented_failures': 0,
        'operational_hours': 0,
        'emergency_stops': 0,
        'total_cycles': 0
    }

def show_landing_page(soul_system):
    """Страница запуска системы"""
    st.info("🧠 **AVCS SOUL Integrated System Ready** - All modules initialized and ready for operation")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.subheader("🔮 Digital Twin")
        st.write("• Real-time Equipment Simulation")
        st.write("• Predictive Behavior Modeling")
        st.write("• Virtual Sensor Data")
        st.write("• Failure Scenario Testing")
    
    with col2:
        st.subheader("🏭 PLC Integration")
        st.write("• Industrial Protocol Support")
        st.write("• Real Equipment Control")
        st.write("• Sensor Data Acquisition")
        st.write("• MR Damper Management")
    
    with col3:
        st.subheader("🎤 Voice AI")
        st.write("• Natural Language Interface")
        st.write("• Emotional Intelligence")
        st.write("• Voice Commands")
        st.write("• Status Announcements")
    
    with col4:
        st.subheader("📊 Unified Analytics")
        st.write("• Integrated Data Fusion")
        st.write("• Cross-Module Intelligence")
        st.write("• Business Metrics")
        st.write("• Predictive Maintenance")

def run_integrated_monitoring(soul_system, status_display, cycle_display, progress_display, speed, max_cycles):
    """Основной цикл integrated мониторинга"""
    current_cycle = st.session_state.current_cycle
    
    if current_cycle < max_cycles and st.session_state.system_running:
        # Генерация данных через integrated system
        vibration, temperature, noise, data_source = soul_system.generate_integrated_sensor_data(
            current_cycle, st.session_state.current_mode
        )
        
        # Расчет метрик
        risk_index = calculate_risk(vibration, temperature, noise)
        rul_hours = calculate_rul(risk_index, current_cycle)
        damper_force = calculate_damper_force(risk_index)
        
        # Обновление performance metrics
        soul_system.performance_metrics['operational_hours'] = current_cycle * 0.1
        soul_system.performance_metrics['total_cycles'] = current_cycle
        
        if risk_index > 80 and st.session_state.current_mode != "normal":
            soul_system.performance_metrics['prevented_failures'] += 1
        
        # Голосовые уведомления
        if current_cycle % 25 == 0:  # Каждые 25 циклов
            soul_system.voice_announcement(
                risk_index, st.session_state.current_mode,
                soul_system.performance_metrics['prevented_failures'],
                rul_hours
            )
        
        # Обновление демпферов
        st.session_state.damper_forces = {damper: damper_force for damper in IndustrialConfig.MR_DAMPERS.keys()}
        
        # Сохранение данных
        update_sensor_data(vibration, temperature, noise)
        st.session_state.risk_history.append(risk_index)
        
        # Обновление дисплеев
        update_integrated_displays(risk_index, rul_hours, current_cycle, max_cycles, data_source,
                                 status_display, cycle_display, progress_display, soul_system)
        
        # Следующий цикл
        st.session_state.current_cycle += 1
        time.sleep(speed)
        st.rerun()
    
    elif current_cycle >= max_cycles:
        st.success("🧠 Integrated AVCS SOUL Simulation Completed Successfully!")
        st.session_state.system_running = False

def update_sensor_data(vibration, temperature, noise):
    """Обновление данных сенсоров"""
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
    
    # Ограничение размера данных
    for data in [st.session_state.vibration_data, st.session_state.temperature_data, 
                 st.session_state.noise_data, st.session_state.damper_data]:
        if len(data) > 50:
            data = data.iloc[1:]
    if len(st.session_state.risk_history) > 50:
        st.session_state.risk_history = st.session_state.risk_history[1:]

def update_integrated_displays(risk_index, rul_hours, current_cycle, max_cycles, data_source,
                             status_display, cycle_display, progress_display, soul_system):
    """Обновление integrated дисплеев"""
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
    
    # Data Source Info
    st.sidebar.markdown("---")
    st.sidebar.info(f"**Data Source:** {data_source}")
    
    # Main Dashboard
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Integrated Monitoring Dashboard")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Vibration", "Temperature", "Noise", "Dampers"])
        
        with tab1:
            if not st.session_state.vibration_data.empty:
                st.plotly_chart(create_sensor_chart(
                    st.session_state.vibration_data, "Vibration Monitoring", "Vibration (mm/s)"
                ), use_container_width=True)
        
        with tab2:
            if not st.session_state.temperature_data.empty:
                st.plotly_chart(create_sensor_chart(
                    st.session_state.temperature_data, "Temperature Monitoring", "Temperature (°C)" 
                ), use_container_width=True)
        
        with tab3:
            if not st.session_state.noise_data.empty:
                st.plotly_chart(create_sensor_chart(
                    st.session_state.noise_data, "Acoustic Monitoring", "Noise (dB)"
                ), use_container_width=True)
        
        with tab4:
            if not st.session_state.damper_data.empty:
                st.plotly_chart(create_sensor_chart(
                    st.session_state.damper_data, "MR Damper Control", "Force (N)"
                ), use_container_width=True)
    
    with col2:
        st.subheader("🎯 System Metrics")
        
        # Risk Gauge
        st.plotly_chart(create_risk_gauge(risk_index), use_container_width=True)
        
        # Performance Metrics
        st.metric("🛡️ Prevented Failures", soul_system.performance_metrics['prevented_failures'])
        st.metric("⏱️ Operational Hours", f"{soul_system.performance_metrics['operational_hours']:.1f}")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if rul_hours < 24:
                st.error(f"⏳ RUL\n{rul_hours}h")
            elif rul_hours < 72:
                st.warning(f"⏳ RUL\n{rul_hours}h") 
            else:
                st.success(f"⏳ RUL\n{rul_hours}h")
            
            st.metric("🔧 Mode", FAILURE_MODES[st.session_state.current_mode]['name'])
        
        with col_b:
            st.metric("📊 Risk", f"{risk_index}%")
            st.metric("🔄 Cycle", current_cycle + 1)
        
        # Damper Status
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
