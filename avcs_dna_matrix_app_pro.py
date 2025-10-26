# avcs_dna_matrix_app_pro.py - AVCS DNA Industrial Monitor v6.0 (Production Ready)
import os
import json
import time
import warnings
import hmac
import hashlib
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

warnings.filterwarnings('ignore')

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
        'DAMPER_FL': 'Front-Left',
        'DAMPER_FR': 'Front-Right',
        'DAMPER_RL': 'Rear-Left',
        'DAMPER_RR': 'Rear-Right'
    }
    VIBRATION_LIMITS = {'normal': 2.0, 'warning': 4.0, 'critical': 6.0}
    TEMPERATURE_LIMITS = {'normal': 70, 'warning': 85, 'critical': 100}
    DAMPER_FORCES = {'standby': 500, 'normal': 1000, 'warning': 4000, 'critical': 8000}

# --- DATA MANAGER ---
class DataManager:
    @staticmethod
    def safe_data_update(data_dict, session_key, max_history=50):
        if session_key not in st.session_state:
            st.session_state[session_key] = pd.DataFrame()
        
        new_data = pd.DataFrame([data_dict])
        st.session_state[session_key] = pd.concat([
            st.session_state[session_key], new_data
        ], ignore_index=True)
        
        if len(st.session_state[session_key]) > max_history:
            st.session_state[session_key] = st.session_state[session_key].iloc[1:]

# --- ENHANCED COMPONENTS ---
class SafetyMonitor:
    def check_emergency_conditions(self, vibration, temperature, noise):
        emergencies = []
        if any(v > 6.0 for v in vibration.values()):
            emergencies.append("Vibration critical")
        if any(t > 100 for t in temperature.values()):
            emergencies.append("Temperature critical")
        if noise > 100:
            emergencies.append("Noise critical")
        return emergencies
    
    def trigger_emergency_shutdown(self, conditions):
        st.session_state.system_running = False
        st.session_state.damper_forces = {d: 0 for d in st.session_state.damper_forces.keys()}

class BusinessIntelligence:
    def calculate_operational_efficiency(self, risk_history):
        if not risk_history:
            return 85.0, 0.1, 0.05
        avg_risk = np.mean(risk_history)
        warning_ratio = len([r for r in risk_history if r > 50]) / len(risk_history)
        critical_ratio = len([r for r in risk_history if r > 80]) / len(risk_history)
        efficiency = max(0, 100 - avg_risk)
        return efficiency, warning_ratio, critical_ratio
    
    def calculate_roi(self, prevented_failures, operational_hours):
        base_cost_per_failure = 50000
        system_cost = 100000
        cost_savings = prevented_failures * base_cost_per_failure
        roi = ((cost_savings - system_cost) / system_cost) * 100 if system_cost > 0 else 0
        return max(0, roi), cost_savings

class EnhancedAIModel:
    def predict(self, features):
        if not features:
            return 1, 0.5
        feature_sum = sum(features)
        feature_count = len(features)
        avg_feature = feature_sum / feature_count
        
        if avg_feature > 5.0:
            prediction = -1
            confidence = min(0.95, avg_feature / 10.0)
        else:
            prediction = 1
            confidence = max(0.5, 1.0 - (avg_feature / 10.0))
        return prediction, confidence

# --- INITIALIZATION ---
def initialize_enhanced_system():
    st.session_state.system_running = False
    st.session_state.data_dict = {
        'vibration': pd.DataFrame(),
        'temperature': pd.DataFrame(),
        'noise': pd.DataFrame(columns=['NOISE']),
        'dampers': pd.DataFrame(),
        'risk_history': []
    }
    st.session_state.performance_metrics = {
        'cycles_completed': 0,
        'emergency_stops': 0,
        'prevented_failures': 0,
        'total_operational_hours': 0
    }
    st.session_state.system_logs = []
    
    st.session_state.config_manager = IndustrialConfig()
    st.session_state.data_manager = DataManager()
    st.session_state.safety_monitor = SafetyMonitor()
    st.session_state.business_intel = BusinessIntelligence()
    st.session_state.enhanced_ai = EnhancedAIModel()
    
    st.session_state.damper_forces = {
        damper: st.session_state.config_manager.DAMPER_FORCES.get('standby', 0)
        for damper in st.session_state.config_manager.VIBRATION_SENSORS.keys()
    }

# --- SENSOR DATA GENERATION ---
def generate_enhanced_sensor_data(current_cycle):
    if current_cycle < 30:
        base_vib, base_temp, base_noise = 1.0, 65, 65
    elif current_cycle < 60:
        base_vib, base_temp, base_noise = 3.0, 75, 75
    else:
        base_vib, base_temp, base_noise = 6.0, 90, 90
    
    vibration = {
        k: max(0.1, base_vib + np.random.normal(0, 0.2))
        for k in st.session_state.config_manager.VIBRATION_SENSORS.keys()
    }
    
    temperature = {
        k: max(20, base_temp + np.random.normal(0, 2))
        for k in st.session_state.config_manager.THERMAL_SENSORS.keys()
    }
    
    noise = max(30, base_noise + np.random.normal(0, 2))
    
    return vibration, temperature, noise

# --- CALCULATIONS ---
def calculate_enhanced_rul(risk_index, current_cycle, vibration, temperature):
    base_rul = max(0, 100 - risk_index)
    if current_cycle > 150:
        degradation_penalty = (current_cycle - 150) * 0.2
        base_rul -= degradation_penalty
    max_vibration = max(vibration.values()) if vibration else 0.0
    max_temperature = max(temperature.values()) if temperature else 0.0
    if max_vibration > 4.0:
        base_rul *= 0.8
    if max_temperature > 85:
        base_rul *= 0.7
    return max(0, int(base_rul))

def calculate_efficiency(risk_index):
    return max(0, 100 - risk_index)

def calculate_damper_force(risk_index, ai_prediction):
    cfg = st.session_state.config_manager.DAMPER_FORCES
    if ai_prediction == -1 or risk_index > 85:
        return cfg.get('critical', 8000)
    elif risk_index > 65:
        return cfg.get('warning', 4000)
    elif risk_index > 30:
        return cfg.get('normal', 1000)
    else:
        return cfg.get('standby', 500)

# --- VISUALIZATIONS ---
def create_risk_gauge(risk_index):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_index,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "AI Risk Index", 'font': {'size': 20}},
        delta={'reference': 50, 'increasing': {'color': "red"}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
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
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=50, b=10))
    return fig

def create_combined_sensor_dashboard(data_dict):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Vibration Sensors', 'Temperature Sensors', 'Noise Level', 'Risk History'),
        vertical_spacing=0.12,
        horizontal_spacing=0.08
    )

    # Vibration sensors
    if 'vibration' in data_dict and not data_dict['vibration'].empty:
        for sensor in data_dict['vibration'].columns:
            human_name = st.session_state.config_manager.VIBRATION_SENSORS.get(sensor, sensor)
            fig.add_trace(
                go.Scatter(
                    y=data_dict['vibration'][sensor],
                    name=human_name,
                    line=dict(width=2),
                    showlegend=True
                ), row=1, col=1
            )
    else:
        fig.add_trace(go.Scatter(x=[], y=[], name="No Vibration Data"), row=1, col=1)

    # Temperature sensors
    if 'temperature' in data_dict and not data_dict['temperature'].empty:
        for sensor in data_dict['temperature'].columns:
            human_name = st.session_state.config_manager.THERMAL_SENSORS.get(sensor, sensor)
            fig.add_trace(
                go.Scatter(
                    y=data_dict['temperature'][sensor],
                    name=human_name,
                    line=dict(width=2),
                    showlegend=True
                ), row=1, col=2
            )
    else:
        fig.add_trace(go.Scatter(x=[], y=[], name="No Temperature Data"), row=1, col=2)

    # Noise level
    if 'noise' in data_dict and not data_dict['noise'].empty and 'NOISE' in data_dict['noise'].columns:
        fig.add_trace(
            go.Scatter(
                y=data_dict['noise']['NOISE'],
                name="Noise Level",
                line=dict(color='purple', width=3),
                showlegend=True
            ),
            row=2, col=1
        )
    else:
        fig.add_trace(go.Scatter(x=[], y=[], name="No Noise Data"), row=2, col=1)

    # Risk history
    if data_dict.get('risk_history'):
        fig.add_trace(
            go.Scatter(
                y=data_dict['risk_history'],
                name="Risk Index",
                line=dict(color='red', width=3),
                showlegend=True
            ),
            row=2, col=2
        )
    else:
        fig.add_trace(go.Scatter(x=[], y=[], name="No Risk Data"), row=2, col=2)

    fig.update_xaxes(title_text="Time", row=1, col=1)
    fig.update_xaxes(title_text="Time", row=1, col=2)
    fig.update_xaxes(title_text="Time", row=2, col=1)
    fig.update_xaxes(title_text="Time", row=2, col=2)
    
    fig.update_yaxes(title_text="Vibration (mm/s)", row=1, col=1)
    fig.update_yaxes(title_text="Temperature (°C)", row=1, col=2)
    fig.update_yaxes(title_text="Noise (dB)", row=2, col=1)
    fig.update_yaxes(title_text="Risk Index", row=2, col=2)

    fig.update_layout(height=600, showlegend=True, title_text="Combined Sensor Dashboard")
    return fig

# --- LANDING PAGE ---
def show_landing_page():
    st.info("🚀 **System Ready** - Click 'Start System' to begin enhanced monitoring")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🎯 Enhanced Features")
        st.write("• Real-time AI Risk Assessment")
        st.write("• Advanced Safety Monitoring")
        st.write("• Business Intelligence")
        st.write("• Multi-sensor Data Fusion")
        st.write("• Predictive Maintenance")

    with col2:
        st.subheader("🛡️ Safety Systems")
        st.write("• Emergency Shutdown Protocols")
        st.write("• Real-time Limit Monitoring")
        st.write("• Failure Prediction")
        st.write("• Automated Damper Control")
        st.write("• System Health Checks")

    with col3:
        st.subheader("📈 Analytics")
        st.write("• Operational Efficiency")
        st.write("• ROI Calculation")
        st.write("• Performance Metrics")
        st.write("• Cost-Benefit Analysis")
        st.write("• Trend Analysis")

# --- MONITORING LOOP ---
def run_enhanced_monitoring_loop(status_indicator, cycle_display, performance_display, simulation_speed, max_cycles):
    current_cycle = len(st.session_state.data_dict.get('risk_history', []))
    progress_bar = st.sidebar.progress(0)

    if not st.session_state.get('system_running'):
        return

    try:
        if current_cycle < max_cycles and st.session_state.system_running:
            vibration, temperature, noise = generate_enhanced_sensor_data(current_cycle)

            # Safety monitoring
            emergency_conditions = st.session_state.safety_monitor.check_emergency_conditions(vibration, temperature, noise)
            if emergency_conditions:
                st.session_state.safety_monitor.trigger_emergency_shutdown(emergency_conditions)
                st.error(f"🚨 EMERGENCY SHUTDOWN: {', '.join(emergency_conditions)}")
                st.session_state.performance_metrics['emergency_stops'] += 1
                return

            # AI analysis
            features = list(vibration.values()) + list(temperature.values()) + [noise]
            ai_prediction, ai_confidence = st.session_state.enhanced_ai.predict(features)
            risk_index = min(100, max(0, int(abs(ai_confidence) * 150 + np.random.normal(0, 5))))
            rul_hours = calculate_enhanced_rul(risk_index, current_cycle, vibration, temperature)

            # Damper control
            damper_force = calculate_damper_force(risk_index, ai_prediction)
            st.session_state.damper_forces = {d: damper_force for d in st.session_state.damper_forces.keys()}

            # Update data
            st.session_state.data_manager.safe_data_update(vibration, 'vibration')
            st.session_state.data_manager.safe_data_update(temperature, 'temperature')
            st.session_state.data_manager.safe_data_update({'NOISE': noise}, 'noise')
            st.session_state.data_manager.safe_data_update(st.session_state.damper_forces, 'dampers')
            
            st.session_state.data_dict['risk_history'].append(risk_index)

            # Update displays
            update_enhanced_displays(risk_index, rul_hours, ai_confidence, current_cycle, max_cycles,
                                   status_indicator, cycle_display, performance_display, progress_bar)

            # Update performance metrics
            st.session_state.performance_metrics['cycles_completed'] = current_cycle + 1
            if risk_index > 80:
                st.session_state.performance_metrics['prevented_failures'] += 1

            time.sleep(max(0.05, float(simulation_speed)))
            st.rerun()

        elif current_cycle >= max_cycles:
            st.success("✅ Enhanced simulation completed successfully!")
            st.session_state.system_running = False
    except Exception as e:
        st.error(f"Monitoring loop error: {e}")
        st.session_state.system_running = False

def update_enhanced_displays(risk_index, rul_hours, ai_confidence, current_cycle, max_cycles,
                           status_indicator, cycle_display, performance_display, progress_bar):
    if risk_index > 80:
        status_color, status_text = "red", "🚨 CRITICAL"
    elif risk_index > 50:
        status_color, status_text = "orange", "⚠️ WARNING"
    elif risk_index > 20:
        status_color, status_text = "green", "✅ NORMAL"
    else:
        status_color, status_text = "blue", "🟢 STANDBY"

    status_indicator.markdown(f"<h3 style='color: {status_color}; text-align: center;'>{status_text}</h3>", unsafe_allow_html=True)
    cycle_display.metric("Current Cycle", f"{current_cycle + 1}/{max_cycles}")
    efficiency = calculate_efficiency(risk_index)
    performance_display.metric("Operational Efficiency", f"{efficiency:.1f}%")
    progress_bar.progress(min(1.0, (current_cycle + 1) / max_cycles))

    # Dashboard layout
    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(create_combined_sensor_dashboard(st.session_state.data_dict), use_container_width=True)
    with col2:
        st.plotly_chart(create_risk_gauge(risk_index), use_container_width=True)

        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            if rul_hours < 24:
                st.error(f"⏳ RUL\n{rul_hours} h")
            elif rul_hours < 72:
                st.warning(f"⏳ RUL\n{rul_hours} h")
            else:
                st.success(f"⏳ RUL\n{rul_hours} h")
            st.metric("🤖 AI Confidence", f"{abs(ai_confidence):.3f}")
        with metric_col2:
            st.metric("📊 Risk Index", f"{risk_index}%")
            st.metric("🔄 Current Cycle", current_cycle + 1)

# --- MAIN APPLICATION ---
def main():
    if "config_manager" not in st.session_state:
        initialize_enhanced_system()

    st.title("🏭 AVCS DNA - Industrial Monitoring System v6.0")
    st.markdown("**Enhanced Active Vibration Control System with AI-Powered Predictive Maintenance**")

    # Sidebar and controls
    st.sidebar.header("🎛️ AVCS DNA Control Panel v6.0")
    
    control_col1, control_col2 = st.sidebar.columns(2)
    with control_col1:
        if st.button("⚡ Start System", type="primary", use_container_width=True):
            st.session_state.system_running = True
            st.session_state.data_dict = {
                'vibration': pd.DataFrame(),
                'temperature': pd.DataFrame(), 
                'noise': pd.DataFrame(columns=['NOISE']),
                'dampers': pd.DataFrame(),
                'risk_history': []
            }
            st.session_state.performance_metrics.update({
                'cycles_completed': 0,
                'emergency_stops': 0,
                'prevented_failures': 0
            })
            st.rerun()
    
    with control_col2:
        if st.button("🛑 Emergency Stop", use_container_width=True):
            st.session_state.system_running = False
            st.session_state.damper_forces = {
                damper: st.session_state.config_manager.DAMPER_FORCES.get('standby', 0)
                for damper in st.session_state.damper_forces.keys()
            }
            st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Simulation Settings")
    simulation_speed = st.sidebar.slider("Simulation Speed", 0.1, 2.0, 0.5, 0.1)
    max_cycles = st.sidebar.slider("Max Cycles", 50, 500, 200, 50)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 System Status")
    status_indicator = st.sidebar.empty()
    cycle_display = st.sidebar.empty()
    performance_display = st.sidebar.empty()
    
    # Business intelligence
    st.sidebar.markdown("---")
    st.sidebar.subheader("💼 Business Intelligence")
    
    if st.session_state.get('business_intel') and st.session_state.data_dict.get('risk_history'):
        efficiency, warning_ratio, critical_ratio = st.session_state.business_intel.calculate_operational_efficiency(
            st.session_state.data_dict['risk_history']
        )
        roi, cost_savings = st.session_state.business_intel.calculate_roi(
            st.session_state.performance_metrics.get('prevented_failures', 0),
            st.session_state.performance_metrics.get('cycles_completed', 0) / 10
        )
        
        st.sidebar.metric("Operational Efficiency", f"{efficiency:.1f}%")
        st.sidebar.metric("ROI", f"{roi:.0f}%")
        st.sidebar.metric("Cost Savings", f"${cost_savings:,.0f}")

    # Main display
    if not st.session_state.system_running:
        show_landing_page()
    else:
        run_enhanced_monitoring_loop(
            status_indicator, cycle_display, performance_display, simulation_speed, max_cycles
        )

    st.markdown("---")
    st.caption("**AVCS DNA Matrix Soul v6.0** | Yeruslan Technologies | Predictive Maintenance System")

if __name__ == "__main__":
    main()
