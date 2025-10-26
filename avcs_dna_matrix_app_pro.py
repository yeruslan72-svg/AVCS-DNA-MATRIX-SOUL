# avcs_dna_matrix_soul.py - ПОЛНАЯ ВЕРСИЯ СО ВСЕМИ ФУНКЦИЯМИ
import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AVCS DNA MATRIX SOUL v6.0",
    layout="wide",
    page_icon="🧠"
)

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
    "normal": {"name": "🟢 Normal Operation", "vib": 1.0, "temp": 65, "noise": 65, "cost_impact": 0},
    "bearing_wear": {"name": "🟠 Bearing Wear", "vib": 5.0, "temp": 80, "noise": 75, "cost_impact": 50000},
    "misalignment": {"name": "🔴 Shaft Misalignment", "vib": 6.0, "temp": 75, "noise": 70, "cost_impact": 35000},
    "imbalance": {"name": "🟣 Rotational Imbalance", "vib": 7.0, "temp": 70, "noise": 80, "cost_impact": 25000},
    "cavitation": {"name": "🔵 Pump Cavitation", "vib": 3.0, "temp": 68, "noise": 90, "cost_impact": 15000}
}

# --- VOICE & EMOTION SYSTEM ---
class VoiceEmotionSystem:
    def __init__(self):
        self.emotional_state = "CALM"
        self.last_speech = None
        self.speech_history = []
        
    def generate_speech(self, risk, mode, prevented_failures):
        emotions = {
            "CALM": ["😊", "Система работает стабильно", "Оптимальные показатели"],
            "ALERT": ["👁️", "Повышенный уровень риска", "Требуется внимание"],
            "URGENT": ["🚨", "Критическая ситуация!", "Немедленное вмешательство"],
            "PROUD": ["🦸", "Отличные результаты!", "Эффективная работа"],
            "CONCERNED": ["😟", "Ухудшение параметров", "Рекомендуется проверка"]
        }
        
        if risk > 85:
            emotion = "URGENT"
            text = f"КРИТИЧЕСКИЙ РИСК! Уровень {risk}%. {FAILURE_MODES[mode]['name']}. Активированы аварийные протоколы."
        elif risk > 60:
            emotion = "ALERT" 
            text = f"ВНИМАНИЕ! Риск повышен до {risk}%. Режим: {FAILURE_MODES[mode]['name']}. Мониторинг усилен."
        elif prevented_failures > 0:
            emotion = "PROUD"
            text = f"УСПЕХ! Предотвращено {prevented_failures} аварий. ROI: {st.session_state.get('current_roi', 0):.0f}%"
        else:
            emotion = "CALM"
            text = f"Стабильная работа. Риск: {risk}%. Режим: {FAILURE_MODES[mode]['name']}"
            
        self.emotional_state = emotion
        return text, emotions[emotion]
    
    def display_emotion(self):
        emotion_data = {
            "CALM": {"emoji": "😊", "color": "green", "text": "Спокоен"},
            "ALERT": {"emoji": "👁️", "color": "orange", "text": "Внимателен"}, 
            "URGENT": {"emoji": "🚨", "color": "red", "text": "Тревога"},
            "PROUD": {"emoji": "🦸", "color": "blue", "text": "Горд"},
            "CONCERNED": {"emoji": "😟", "color": "yellow", "text": "Озабочен"}
        }
        
        data = emotion_data[self.emotional_state]
        st.sidebar.markdown(f"""
        <div style="background: {data['color']}20; padding: 15px; border-radius: 10px; border-left: 4px solid {data['color']};">
            <div style="font-size: 24px; text-align: center;">{data['emoji']}</div>
            <div style="text-align: center; font-weight: bold;">{data['text']}</div>
            <div style="text-align: center; font-size: 12px;">{self.emotional_state}</div>
        </div>
        """, unsafe_allow_html=True)

# --- BUSINESS INTELLIGENCE ---
class BusinessIntelligence:
    def __init__(self):
        self.system_cost = 250000
        self.operational_costs = 5000
        self.failure_costs = {
            "normal": 0,
            "bearing_wear": 75000, 
            "misalignment": 50000,
            "imbalance": 35000,
            "cavitation": 20000
        }
        
    def calculate_roi(self, operational_hours, prevented_failures, current_mode):
        operational_savings = operational_hours * 100
        failure_savings = prevented_failures * self.failure_costs.get(current_mode, 50000)
        total_savings = operational_savings + failure_savings
        roi = ((total_savings - self.system_cost) / self.system_cost) * 100
        return max(0, roi), total_savings
    
    def generate_report(self, metrics, sensor_data):
        report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operational_efficiency": metrics.get('efficiency', 0),
            "roi_percentage": metrics.get('roi', 0),
            "cost_savings": metrics.get('savings', 0),
            "prevented_failures": metrics.get('prevented_failures', 0),
            "risk_level": metrics.get('risk', 0),
            "recommendations": self.generate_recommendations(metrics)
        }
        return report
    
    def generate_recommendations(self, metrics):
        recs = []
        if metrics.get('risk', 0) > 80:
            recs.append("НЕМЕДЛЕННЫЙ РЕМОНТ - Критический уровень риска")
        if metrics.get('risk', 0) > 60:
            recs.append("Плановый ремонт в течение 72 часов")
        if metrics.get('efficiency', 0) < 80:
            recs.append("Оптимизация рабочих параметров")
        if metrics.get('prevented_failures', 0) > 0:
            recs.append(f"Экономия: ${metrics.get('savings', 0):,} благодаря предиктивному обслуживанию")
        return recs

# --- INITIALIZATION ---
def initialize_system():
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
    if "voice_system" not in st.session_state:
        st.session_state.voice_system = VoiceEmotionSystem()
    if "business_intel" not in st.session_state:
        st.session_state.business_intel = BusinessIntelligence()
    if "performance_metrics" not in st.session_state:
        st.session_state.performance_metrics = {
            'prevented_failures': 0,
            'operational_hours': 0,
            'emergency_stops': 0,
            'total_cycles': 0
        }
    if "reports" not in st.session_state:
        st.session_state.reports = []

# --- SENSOR DATA GENERATION ---
def generate_sensor_data(cycle, failure_mode):
    mode_data = FAILURE_MODES[failure_mode]
    
    # Progressive degradation
    progress = min(1.0, cycle / 100)
    vib_multiplier = 1.0 + progress * 2.0
    temp_multiplier = 1.0 + progress * 0.5
    
    vibration = {}
    for i, sensor in enumerate(IndustrialConfig.VIBRATION_SENSORS.keys()):
        base_vib = mode_data["vib"] * vib_multiplier
        variation = 0.2 + i * 0.1
        vibration[sensor] = max(0.1, base_vib + np.random.normal(0, variation))
    
    temperature = {}
    for i, sensor in enumerate(IndustrialConfig.THERMAL_SENSORS.keys()):
        base_temp = mode_data["temp"] * temp_multiplier
        variation = 1.0 + i * 0.5
        temperature[sensor] = max(20, base_temp + np.random.normal(0, variation))
    
    noise = max(30, mode_data["noise"] + np.random.normal(0, 2))
    
    return vibration, temperature, noise

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
    initialize_system()
    
    st.title("🧠 AVCS DNA MATRIX SOUL v6.0")
    st.markdown("**AI-Powered Industrial Consciousness with Emotional Intelligence**")
    
    # Sidebar
    st.sidebar.header("🎛️ SOUL Control Panel")
    
    # Emotional State Display
    st.sidebar.subheader("🧠 Emotional State")
    st.session_state.voice_system.display_emotion()
    
    # Failure mode selection
    st.sidebar.subheader("🔧 Failure Mode")
    for mode_key, mode_data in FAILURE_MODES.items():
        if st.sidebar.button(mode_data["name"], use_container_width=True):
            st.session_state.current_mode = mode_key
            st.rerun()
    
    st.sidebar.write(f"**Active:** {FAILURE_MODES[st.session_state.current_mode]['name']}")
    
    # Voice Control
    st.sidebar.subheader("🎤 Voice Control")
    if st.sidebar.button("🔊 Speak Status", use_container_width=True):
        risk = st.session_state.risk_history[-1] if st.session_state.risk_history else 0
        text, emotion = st.session_state.voice_system.generate_speech(
            risk, st.session_state.current_mode, 
            st.session_state.performance_metrics['prevented_failures']
        )
        st.sidebar.info(f"**AI:** {text}")
    
    # Control buttons
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("⚡ Start SOUL", type="primary", use_container_width=True):
            st.session_state.system_running = True
            reset_system()
            st.rerun()
    
    with col2:
        if st.button("🛑 Stop System", use_container_width=True):
            st.session_state.system_running = False
            st.session_state.damper_forces = {damper: 500 for damper in IndustrialConfig.MR_DAMPERS.keys()}
            st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Settings")
    simulation_speed = st.sidebar.slider("Speed", 0.1, 2.0, 0.5, 0.1)
    max_cycles = st.sidebar.slider("Max Cycles", 50, 500, 200, 50)
    
    # Business Intelligence
    st.sidebar.markdown("---")
    st.sidebar.subheader("💼 Business Intelligence")
    
    if st.session_state.performance_metrics['operational_hours'] > 0:
        roi, savings = st.session_state.business_intel.calculate_roi(
            st.session_state.performance_metrics['operational_hours'],
            st.session_state.performance_metrics['prevented_failures'],
            st.session_state.current_mode
        )
        st.session_state.current_roi = roi
        st.session_state.current_savings = savings
        
        st.sidebar.metric("💰 ROI", f"{roi:.0f}%")
        st.sidebar.metric("💵 Total Savings", f"${savings:,.0f}")
        st.sidebar.metric("🛡️ Prevented Failures", st.session_state.performance_metrics['prevented_failures'])
    
    # Report Generation
    if st.sidebar.button("📊 Generate Report", use_container_width=True):
        generate_business_report()
    
    # Status
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 System Status")
    status_display = st.sidebar.empty()
    cycle_display = st.sidebar.empty()
    progress_display = st.sidebar.empty()
    
    # Main display
    if not st.session_state.system_running:
        show_landing_page()
    else:
        run_soul_monitoring_loop(status_display, cycle_display, progress_display, simulation_speed, max_cycles)

def reset_system():
    st.session_state.vibration_data = pd.DataFrame(columns=list(IndustrialConfig.VIBRATION_SENSORS.keys()))
    st.session_state.temperature_data = pd.DataFrame(columns=list(IndustrialConfig.THERMAL_SENSORS.keys()))
    st.session_state.noise_data = pd.DataFrame(columns=['NOISE'])
    st.session_state.damper_data = pd.DataFrame(columns=list(IndustrialConfig.MR_DAMPERS.keys()))
    st.session_state.risk_history = []
    st.session_state.current_cycle = 0
    st.session_state.performance_metrics = {
        'prevented_failures': 0,
        'operational_hours': 0,
        'emergency_stops': 0,
        'total_cycles': 0
    }

def generate_business_report():
    if st.session_state.risk_history:
        current_risk = st.session_state.risk_history[-1]
    else:
        current_risk = 0
        
    report = st.session_state.business_intel.generate_report({
        'risk': current_risk,
        'efficiency': 100 - current_risk,
        'roi': st.session_state.get('current_roi', 0),
        'savings': st.session_state.get('current_savings', 0),
        'prevented_failures': st.session_state.performance_metrics['prevented_failures']
    }, st.session_state.vibration_data)
    
    st.session_state.reports.append(report)
    
    # Display report
    st.success("📊 Business Report Generated!")
    with st.expander("View Full Report"):
        st.json(report)

def show_landing_page():
    st.info("🧠 **AVCS SOUL System Ready** - Select failure mode and activate consciousness")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.subheader("🧠 AI Consciousness")
        st.write("• Emotional Intelligence")
        st.write("• Voice Communication") 
        st.write("• Predictive Analytics")
        st.write("• Adaptive Learning")
    
    with col2:
        st.subheader("🏭 Industrial Monitoring")
        st.write("• 4x Vibration Sensors")
        st.write("• 4x Thermal Sensors")
        st.write("• Acoustic Analysis")
        st.write("• MR Damper Control")
    
    with col3:
        st.subheader("💼 Business Intelligence")
        st.write("• ROI Calculation")
        st.write("• Cost-Benefit Analysis")
        st.write("• Automated Reporting")
        st.write("• Performance Metrics")
    
    with col4:
        st.subheader("🛡️ Safety Systems")
        st.write("• Emergency Protocols")
        st.write("• Risk Assessment")
        st.write("• Preventive Maintenance")
        st.write("• Failure Prediction")

def run_soul_monitoring_loop(status_display, cycle_display, progress_display, speed, max_cycles):
    current_cycle = st.session_state.current_cycle
    
    if current_cycle < max_cycles and st.session_state.system_running:
        # Generate data
        vibration, temperature, noise = generate_sensor_data(current_cycle, st.session_state.current_mode)
        
        # Calculate metrics
        risk_index = calculate_risk(vibration, temperature, noise)
        rul_hours = calculate_rul(risk_index, current_cycle)
        damper_force = calculate_damper_force(risk_index)
        
        # Update performance metrics
        st.session_state.performance_metrics['operational_hours'] = current_cycle * 0.1
        st.session_state.performance_metrics['total_cycles'] = current_cycle
        
        if risk_index > 80 and st.session_state.current_mode != "normal":
            st.session_state.performance_metrics['prevented_failures'] += 1
        
        # Voice announcements
        if current_cycle % 25 == 0:  # Every 25 cycles
            text, emotion = st.session_state.voice_system.generate_speech(
                risk_index, st.session_state.current_mode,
                st.session_state.performance_metrics['prevented_failures']
            )
            st.info(f"**🧠 AI Voice:** {text}")
        
        # Update damper forces
        st.session_state.damper_forces = {damper: damper_force for damper in IndustrialConfig.MR_DAMPERS.keys()}
        
        # Store data
        update_sensor_data(vibration, temperature, noise)
        st.session_state.risk_history.append(risk_index)
        
        # Update displays
        update_soul_displays(risk_index, rul_hours, current_cycle, max_cycles, status_display, cycle_display, progress_display)
        
        # Next cycle
        st.session_state.current_cycle += 1
        time.sleep(speed)
        st.rerun()
    
    elif current_cycle >= max_cycles:
        st.success("🧠 SOUL Simulation Completed - Consciousness Cycle Finished")
        st.session_state.system_running = False

def update_sensor_data(vibration, temperature, noise):
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
    
    # Limit data size
    for data in [st.session_state.vibration_data, st.session_state.temperature_data, 
                 st.session_state.noise_data, st.session_state.damper_data]:
        if len(data) > 50:
            data = data.iloc[1:]
    if len(st.session_state.risk_history) > 50:
        st.session_state.risk_history = st.session_state.risk_history[1:]

def update_soul_displays(risk_index, rul_hours, current_cycle, max_cycles, status_display, cycle_display, progress_display):
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
    cycle_display.metric("Consciousness Cycle", f"{current_cycle + 1}/{max_cycles}")
    progress_display.progress((current_cycle + 1) / max_cycles)
    
    # Main Dashboard
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 SOUL Monitoring Dashboard")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Vibration", "Temperature", "Noise", "Dampers"])
        
        with tab1:
            if not st.session_state.vibration_data.empty:
                st.plotly_chart(create_sensor_chart(
                    st.session_state.vibration_data, "Vibration Consciousness", "Vibration (mm/s)"
                ), use_container_width=True)
        
        with tab2:
            if not st.session_state.temperature_data.empty:
                st.plotly_chart(create_sensor_chart(
                    st.session_state.temperature_data, "Thermal Awareness", "Temperature (°C)" 
                ), use_container_width=True)
        
        with tab3:
            if not st.session_state.noise_data.empty:
                st.plotly_chart(create_sensor_chart(
                    st.session_state.noise_data, "Acoustic Perception", "Noise (dB)"
                ), use_container_width=True)
        
        with tab4:
            if not st.session_state.damper_data.empty:
                st.plotly_chart(create_sensor_chart(
                    st.session_state.damper_data, "MR Damper Control", "Force (N)"
                ), use_container_width=True)
    
    with col2:
        st.subheader("🎯 SOUL Metrics")
        
        # Risk gauge
        st.plotly_chart(create_risk_gauge(risk_index), use_container_width=True)
        
        # Business metrics
        st.metric("💰 ROI", f"{st.session_state.get('current_roi', 0):.0f}%")
        st.metric("💵 Savings", f"${st.session_state.get('current_savings', 0):,.0f}")
        
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
            st.metric("🛡️ Prevented", st.session_state.performance_metrics['prevented_failures'])
        
        # Damper status
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
