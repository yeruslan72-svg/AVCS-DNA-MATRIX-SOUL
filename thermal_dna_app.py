import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta
import pandas as pd
import json

st.set_page_config(page_title="FPSO DNA Suite", layout="wide", page_icon="🏭")

# ==================== ADVANCED CONFIGURATION ====================
class SystemConfig:
    # Thermal DNA
    THERMAL_SENSORS = 8
    TEMP_NORMAL = (40, 60)
    TEMP_WARNING = (61, 80)  
    TEMP_CRITICAL = (81, 120)
    
    # AVCS DNA
    VIB_SENSORS = 4
    VIB_NORMAL = (0, 2.0)
    VIB_WARNING = (2.1, 4.0)
    VIB_CRITICAL = (4.1, 10.0)
    
    # Business
    DOWNTIME_COST_PER_HOUR = 75000  # $
    SYSTEM_COST = 250000  # $
    MAINTENANCE_COST_CRITICAL = 50000  # $
    MAINTENANCE_COST_PREVENTIVE = 15000  # $

# ==================== AI ANOMALY DETECTION ====================
class ThermalDNAAnalyzer:
    def __init__(self):
        self.temperature_history = []
        self.anomaly_scores = []
        
    def detect_anomalies(self, current_temp, sensor_id):
        """AI-детекция thermal аномалий"""
        if len(self.temperature_history) < 10:
            return 0.0
            
        recent_temps = self.temperature_history[-10:]
        trend = np.polyfit(range(len(recent_temps)), recent_temps, 1)[0]
        volatility = np.std(recent_temps)
        
        # AI логика обнаружения аномалий
        anomaly_score = 0.0
        if trend > 0.5:  # Быстрый рост
            anomaly_score += 0.6
        if volatility > 3.0:  # Высокая волатильность
            anomaly_score += 0.4
        if current_temp > 75:  # Абсолютное значение
            anomaly_score += 0.3
            
        return min(anomaly_score, 1.0)

class AVCSDNAAnalyzer:
    def __init__(self):
        self.vibration_history = []
        
    def detect_mechanical_faults(self, current_vib, sensor_id):
        """AI-детекция механических неисправностей"""
        if len(self.vibration_history) < 8:
            return 0.0
            
        recent_vibs = self.vibration_history[-8:]
        spectral_energy = np.sum(np.abs(np.fft.fft(recent_vibs)))
        pattern_consistency = 1.0 / (np.std(recent_vibs) + 0.1)
        
        fault_score = 0.0
        if spectral_energy > 50:
            fault_score += 0.5
        if pattern_consistency < 0.3:
            fault_score += 0.3
        if current_vib > 3.0:
            fault_score += 0.4
            
        return min(fault_score, 1.0)

# ==================== MULTI-SENSOR SIMULATION ====================
def generate_thermal_sensor_data(cycle: int, sensor_id: int) -> float:
    """Реалистичная симуляция multi-sensor thermal данных"""
    base_pattern = {
        0: lambda c: 55 + 2 * np.sin(c * 0.1) + np.random.normal(0, 1),
        1: lambda c: 58 + 3 * np.sin(c * 0.15) + np.random.normal(0, 1.2),
        2: lambda c: 52 + 1.5 * np.sin(c * 0.08) + np.random.normal(0, 0.8),
        3: lambda c: 60 + 2.5 * np.sin(c * 0.12) + np.random.normal(0, 1.1)
    }
    
    # Введение аномалий в определенные циклы
    if cycle > 25 and sensor_id == 1:  # Первый сенсор показывает проблему
        anomaly = max(0, (cycle - 25) * 0.8)
        return base_pattern[sensor_id % 4](cycle) + anomaly + np.random.normal(0, 2)
    elif cycle > 35 and sensor_id == 3:  # Третий сенсор тоже
        anomaly = max(0, (cycle - 35) * 0.6)
        return base_pattern[sensor_id % 4](cycle) + anomaly + np.random.normal(0, 1.5)
    
    return base_pattern[sensor_id % 4](cycle)

def generate_vibration_sensor_data(cycle: int, sensor_id: int) -> float:
    """Реалистичная симуляция multi-sensor vibration данных"""
    base_level = {
        0: 1.2, 1: 1.4, 2: 1.1, 3: 1.3
    }
    
    if cycle > 30:
        # Постепенное ухудшение вибрации
        degradation = min(5.0, (cycle - 30) * 0.15)
        return base_level[sensor_id] + degradation + np.random.normal(0, 0.3)
    
    return base_level[sensor_id] + np.random.normal(0, 0.2)

# ==================== FUSION AI ANALYSIS ====================
def perform_fusion_analysis(thermal_data, vibration_data, cycle):
    """AI-анализ слияния thermal и vibration данных"""
    thermal_anomalies = []
    vibration_anomalies = []
    
    for sensor_id in range(SystemConfig.THERMAL_SENSORS):
        temp = thermal_data[sensor_id]
        anomaly_score = thermal_analyzer.detect_anomalies(temp, sensor_id)
        thermal_anomalies.append(anomaly_score)
        
    for sensor_id in range(SystemConfig.VIB_SENSORS):
        vib = vibration_data[sensor_id]
        fault_score = avcs_analyzer.detect_mechanical_faults(vib, sensor_id)
        vibration_anomalies.append(fault_score)
    
    # Fusion логика
    max_thermal_anomaly = max(thermal_anomalies) if thermal_anomalies else 0
    max_vibration_anomaly = max(vibration_anomalies) if vibration_anomalies else 0
    
    fusion_confidence = max(max_thermal_anomaly, max_vibration_anomaly)
    
    # Определение типа проблемы
    problem_type = "Normal"
    if fusion_confidence > 0.7:
        if max_thermal_anomaly > max_vibration_anomaly:
            problem_type = "Thermal Stress"
        else:
            problem_type = "Mechanical Fault"
    elif fusion_confidence > 0.4:
        problem_type = "Early Warning"
    
    return {
        "fusion_confidence": fusion_confidence,
        "problem_type": problem_type,
        "thermal_anomalies": thermal_anomalies,
        "vibration_anomalies": vibration_anomalies,
        "recommended_action": generate_maintenance_recommendation(
            fusion_confidence, problem_type, cycle
        )
    }

def generate_maintenance_recommendation(confidence, problem_type, cycle):
    """Генерация интеллектуальных рекомендаций"""
    if confidence > 0.8:
        return {
            "action": "IMMEDIATE_SHUTDOWN",
            "priority": "CRITICAL",
            "estimated_savings": SystemConfig.DOWNTIME_COST_PER_HOUR * 24,
            "message": f"Critical {problem_type} detected. Immediate shutdown prevents catastrophic failure."
        }
    elif confidence > 0.6:
        return {
            "action": "SCHEDULE_MAINTENANCE_24H",
            "priority": "HIGH", 
            "estimated_savings": SystemConfig.DOWNTIME_COST_PER_HOUR * 8,
            "message": f"Advanced warning of {problem_type}. Schedule maintenance within 24 hours."
        }
    elif confidence > 0.4:
        return {
            "action": "INCREASE_MONITORING",
            "priority": "MEDIUM",
            "estimated_savings": SystemConfig.MAINTENANCE_COST_PREVENTIVE,
            "message": f"Early signs of {problem_type}. Increase monitoring frequency."
        }
    else:
        return {
            "action": "CONTINUE_MONITORING", 
            "priority": "LOW",
            "estimated_savings": 0,
            "message": "All systems operating normally."
        }

# ==================== ADVANCED VISUALIZATION ====================
def create_thermal_heatmap(thermal_data, cycle):
    """Создание интерактивной тепловой карты"""
    fig = go.Figure(data=go.Heatmap(
        z=[thermal_data],
        y=['Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4', 'Sensor 5', 'Sensor 6', 'Sensor 7', 'Sensor 8'],
        colorscale='RdBu_r',
        zmin=40,
        zmax=100,
        hoverinfo='z',
        showscale=True
    ))
    
    fig.update_layout(
        title=f"Thermal DNA - Sensor Array (Cycle {cycle})",
        xaxis_title="Time",
        yaxis_title="Sensor ID",
        height=300
    )
    
    return fig

def create_vibration_radar(vibration_data):
    """Создание radar chart для вибрационных данных"""
    fig = go.Figure(data=go.Scatterpolar(
        r=vibration_data + [vibration_data[0]],  # Замыкаем круг
        theta=[f'Sensor {i+1}' for i in range(len(vibration_data))] + ['Sensor 1'],
        fill='toself',
        line=dict(color='blue')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 8])
        ),
        showlegend=False,
        title="AVCS DNA - Vibration Profile",
        height=300
    )
    
    return fig

def create_fusion_timeline(thermal_history, vibration_history):
    """Создание timeline fusion анализа"""
    cycles = list(range(len(thermal_history)))
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Thermal data
    fig.add_trace(
        go.Scatter(x=cycles, y=thermal_history, name="Max Temperature", line=dict(color='red')),
        secondary_y=False,
    )
    
    # Vibration data 
    fig.add_trace(
        go.Scatter(x=cycles, y=[v * 10 for v in vibration_history], name="Max Vibration (x10)", line=dict(color='blue')),
        secondary_y=False,
    )
    
    fig.update_layout(
        title="Fusion Analysis Timeline",
        xaxis_title="Cycle",
        height=300
    )
    
    fig.update_yaxes(title_text="Temperature (°C)", secondary_y=False)
    fig.update_yaxes(title_text="Vibration (mm/s)", secondary_y=True)
    
    return fig

# ==================== BUSINESS INTELLIGENCE ====================
def calculate_business_metrics(maintenance_events, total_cycles):
    """Расчет бизнес-метрик ROI"""
    prevented_downtime = sum(event['savings'] for event in maintenance_events)
    maintenance_costs = len(maintenance_events) * SystemConfig.MAINTENANCE_COST_PREVENTIVE
    
    net_savings = prevented_downtime - maintenance_costs
    roi = (net_savings / SystemConfig.SYSTEM_COST) * 100
    
    metrics = {
        'prevented_downtime_cost': prevented_downtime,
        'maintenance_costs': maintenance_costs,
        'net_savings': net_savings,
        'roi_percentage': roi,
        'payback_period': SystemConfig.SYSTEM_COST / (net_savings / total_cycles * 100) if net_savings > 0 else float('inf'),
        'downtime_events_prevented': len([e for e in maintenance_events if e['priority'] == 'CRITICAL'])
    }
    
    return metrics

# ==================== STREAMLIT UI ENHANCEMENTS ====================
def initialize_session_state():
    """Инициализация расширенного state management"""
    defaults = {
        'thermal_data': [],
        'vibration_data': [],
        'fusion_analysis': [],
        'maintenance_events': [],
        'business_metrics': {},
        'system_health': 100.0,
        'current_cycle': 0,
        'simulation_running': False,
        'cost_savings': 0
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Инициализация аналитиков
thermal_analyzer = ThermalDNAAnalyzer()
avcs_analyzer = AVCSDNAAnalyzer()

# Запуск инициализации
initialize_session_state()

# ==================== MAIN STREAMLIT APP ====================
st.title("🏭 FPSO DNA Suite - Industrial AI Monitoring Platform")
st.markdown("""
**Enterprise-grade predictive maintenance system integrating Thermal DNA + AVCS DNA**
*Real-time anomaly detection • Fusion AI analysis • ROI optimization*
""")

# Основной layout
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("🎛️ Control Panel")
    
    control_col1, control_col2, control_col3 = st.columns(3)
    
    with control_col1:
        if st.button("🚀 Start Simulation", type="primary", use_container_width=True):
            st.session_state.simulation_running = True
            st.session_state.current_cycle = 0
            st.session_state.thermal_data = []
            st.session_state.vibration_data = []
            st.session_state.fusion_analysis = []
            st.session_state.maintenance_events = []
            st.session_state.cost_savings = 0
            
    with control_col2:
        if st.button("⏹️ Stop Simulation", use_container_width=True):
            st.session_state.simulation_running = False
            
    with control_col3:
        simulation_speed = st.slider("Simulation Speed", 1, 5, 3)

with col2:
    st.subheader("📊 System Health")
    
    health_col1, health_col2 = st.columns(2)
    
    with health_col1:
        st.metric("Overall Health", f"{st.session_state.system_health:.1f}%")
        
    with health_col2:
        st.metric("Cost Savings", f"${st.session_state.cost_savings:,}")

# Вкладки для различных визуализаций
tab1, tab2, tab3, tab4 = st.tabs(["🌡️ Thermal DNA", "📈 AVCS DNA", "🔍 Fusion AI", "💰 Business Intelligence"])

# Главный симуляционный цикл
if st.session_state.simulation_running:
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for cycle in range(100):  # Увеличили до 100 циклов
        if not st.session_state.simulation_running:
            break
            
        st.session_state.current_cycle = cycle
        
        # Генерация данных
        thermal_readings = [generate_thermal_sensor_data(cycle, i) for i in range(SystemConfig.THERMAL_SENSORS)]
        vibration_readings = [generate_vibration_sensor_data(cycle, i) for i in range(SystemConfig.VIB_SENSORS)]
        
        st.session_state.thermal_data.append(thermal_readings)
        st.session_state.vibration_data.append(vibration_readings)
        
        # AI анализ
        fusion_result = perform_fusion_analysis(thermal_readings, vibration_readings, cycle)
        st.session_state.fusion_analysis.append(fusion_result)
        
        # Обработка maintenance events
        if fusion_result['fusion_confidence'] > 0.6:
            maintenance_event = {
                'cycle': cycle,
                'problem_type': fusion_result['problem_type'],
                'confidence': fusion_result['fusion_confidence'],
                'priority': fusion_result['recommended_action']['priority'],
                'savings': fusion_result['recommended_action']['estimated_savings'],
                'timestamp': datetime.now() + timedelta(minutes=cycle)
            }
            st.session_state.maintenance_events.append(maintenance_event)
            st.session_state.cost_savings += maintenance_event['savings']
        
        # Обновление UI
        progress_bar.progress((cycle + 1) / 100)
        status_text.text(f"Cycle {cycle + 1}/100 - Processing...")
        
        # Real-time визуализации
        with tab1:
            st.plotly_chart(create_thermal_heatmap(thermal_readings, cycle), use_container_width=True)
            
        with tab2:
            st.plotly_chart(create_vibration_radar(vibration_readings), use_container_width=True)
            
        with tab3:
            if len(st.session_state.thermal_data) > 1:
                max_temps = [max(cycle_data) for cycle_data in st.session_state.thermal_data]
                max_vibs = [max(cycle_data) for cycle_data in st.session_state.vibration_data]
                st.plotly_chart(create_fusion_timeline(max_temps, max_vibs), use_container_width=True)
        
        with tab4:
            if st.session_state.maintenance_events:
                metrics = calculate_business_metrics(
                    st.session_state.maintenance_events, 
                    cycle + 1
                )
                
                col1, col2, col3 = st.columns(3)
                col1.metric("ROI", f"{metrics['roi_percentage']:.0f}%")
                col2.metric("Net Savings", f"${metrics['net_savings']:,.0f}")
                col3.metric("Failures Prevented", metrics['downtime_events_prevented'])
        
        # Задержка для real-time эффекта
        time.sleep(0.5 / simulation_speed)
    
    # Финальный отчет
    st.success("🎉 Simulation Completed!")
    
    # Детальный анализ
    st.subheader("📋 Detailed Analysis Report")
    
    if st.session_state.maintenance_events:
        events_df = pd.DataFrame(st.session_state.maintenance_events)
        st.dataframe(events_df, use_container_width=True)
        
        # Визуализация событий во времени
        fig = px.scatter(events_df, x='cycle', y='confidence', color='priority',
                        size='savings', hover_data=['problem_type'])
        st.plotly_chart(fig, use_container_width=True)

# Боковая панель с системной информацией
with st.sidebar:
    st.header("System Information")
    
    st.subheader("🛠️ Configuration")
    st.write(f"• Thermal Sensors: {SystemConfig.THERMAL_SENSORS}")
    st.write(f"• Vibration Sensors: {SystemConfig.VIB_SENSORS}")
    st.write(f"• System Cost: ${SystemConfig.SYSTEM_COST:,}")
    
    st.subheader("📈 Performance")
    if st.session_state.fusion_analysis:
        latest_analysis = st.session_state.fusion_analysis[-1]
        st.write(f"Fusion Confidence: {latest_analysis['fusion_confidence']:.2f}")
        st.write(f"Problem Type: {latest_analysis['problem_type']}")
        
    st.subheader("🔔 Alerts")
    if st.session_state.maintenance_events:
        critical_events = [e for e in st.session_state.maintenance_events if e['priority'] == 'CRITICAL']
        if critical_events:
            st.error(f"🚨 {len(critical_events)} Critical Events")
        else:
            st.success("✅ No Critical Events")

# Footer
st.markdown("---")
st.markdown("**FPSO DNA Suite** • Industrial AI Monitoring Platform • © 2024 Yeruslan Technologies")
