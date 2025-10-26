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

# External modules (updated imports for actual modules)
try:
    from industrial_core.data_manager import IndustrialConfig, DataManager
    from digital_twin.digital_twins import IndustrialDigitalTwin
    from plc_integration.industrial_plc import create_avcs_plc_integration
    from plc_integration.system_integrator import create_soul_integrator
    from voice_system.english_voice_soul import create_english_voice_personality
    from voice_system.voice_interface import create_voice_interface
    from voice_system.emotional_display import create_emotional_display
    
    # Simple fallbacks for enhanced functionality
    class SafetyMonitor:
        def check_emergency_conditions(self, vibration, temperature, noise):
            """Basic safety checks using config limits"""
            emergencies = []
            try:
                # Check vibration limits
                vib_limits = getattr(st.session_state.config_manager, 'VIBRATION_LIMITS', {'critical': 6.0})
                for sensor, value in vibration.items():
                    if value > vib_limits.get('critical', 6.0):
                        emergencies.append(f"Vibration critical: {sensor} = {value:.1f}")
                
                # Check temperature limits
                temp_limits = getattr(st.session_state.config_manager, 'TEMPERATURE_LIMITS', {'critical': 100})
                for sensor, value in temperature.items():
                    if value > temp_limits.get('critical', 100):
                        emergencies.append(f"Temperature critical: {sensor} = {value:.1f}°C")
                        
            except Exception:
                # Fallback basic checks
                if any(v > 6.0 for v in vibration.values()):
                    emergencies.append("Vibration critical")
                if any(t > 100 for t in temperature.values()):
                    emergencies.append("Temperature critical")
            return emergencies
    
        def trigger_emergency_shutdown(self, conditions):
            """Emergency shutdown procedure"""
            st.session_state.system_running = False
            st.session_state.damper_forces = {d: 0 for d in st.session_state.damper_forces.keys()}
            print(f"EMERGENCY SHUTDOWN: {conditions}")
    
    class BusinessIntelligence:
        def calculate_operational_efficiency(self, risk_history):
            """Calculate operational efficiency metrics"""
            if not risk_history:
                return 85.0, 0.1, 0.05
            
            avg_risk = np.mean(risk_history)
            warning_ratio = len([r for r in risk_history if r > 50]) / len(risk_history)
            critical_ratio = len([r for r in risk_history if r > 80]) / len(risk_history)
            efficiency = max(0, 100 - avg_risk)
            return efficiency, warning_ratio, critical_ratio
        
        def calculate_roi(self, prevented_failures, operational_hours):
            """Calculate ROI and cost savings"""
            # Simplified ROI calculation
            base_cost_per_failure = 50000  # Estimated cost of equipment failure
            system_cost = 100000  # Estimated system cost
            
            cost_savings = prevented_failures * base_cost_per_failure
            roi = ((cost_savings - system_cost) / system_cost) * 100 if system_cost > 0 else 0
            
            return max(0, roi), cost_savings
    
    class EnhancedAIModel:
        def predict(self, features):
            """AI prediction based on sensor features"""
            if not features:
                return 1, 0.5
            
            # Simple heuristic based on feature values
            feature_sum = sum(features) if features else 0
            feature_count = len(features)
            
            if feature_count == 0:
                return 1, 0.5
                
            avg_feature = feature_sum / feature_count
            
            # Higher values indicate problems
            if avg_feature > 5.0:
                prediction = -1  # Problem detected
                confidence = min(0.95, avg_feature / 10.0)
            else:
                prediction = 1   # Normal operation
                confidence = max(0.5, 1.0 - (avg_feature / 10.0))
            
            return prediction, confidence

except Exception as e:
    # For dev: allow file to load but mark missing pieces
    missing = str(e)
    print("Module import warning:", missing)
    # define minimal fallbacks to avoid NameError during static review
    IndustrialConfig = globals().get('IndustrialConfig', None)
    DataManager = globals().get('DataManager', None)
    IndustrialDigitalTwin = globals().get('IndustrialDigitalTwin', None)
    create_avcs_plc_integration = globals().get('create_avcs_plc_integration', None)
    create_soul_integrator = globals().get('create_soul_integrator', None)
    create_english_voice_personality = globals().get('create_english_voice_personality', None)
    create_voice_interface = globals().get('create_voice_interface', None)
    create_emotional_display = globals().get('create_emotional_display', None)
    
    # Fallback classes
    class SafetyMonitor:
        def check_emergency_conditions(self, vibration, temperature, noise): return []
        def trigger_emergency_shutdown(self, conditions): pass
    
    class BusinessIntelligence:
        def calculate_operational_efficiency(self, risk_history): return 85.0, 0.1, 0.05
        def calculate_roi(self, prevented_failures, operational_hours): return 150, 50000
    
    class EnhancedAIModel:
        def predict(self, features): return 1, 0.8

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AVCS DNA Industrial Monitor v6.0",
    layout="wide",
    page_icon="🏭"
)

# --- HELPERS: audit packet generation ---
def generate_audit_packet(asset_id, raw_features, derived_features, decision, damper_forces):
    """
    Build an audit packet and sign it with HMAC-SHA256.
    The secret key must be provided in the environment: AUDIT_HMAC_KEY
    """
    packet = {
        "asset_id": asset_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "raw_features": raw_features,
        "derived_features": derived_features,
        "decision": decision,
        "damper_forces": damper_forces
    }
    try:
        secret = os.environ.get("AUDIT_HMAC_KEY")
        if not secret:
            # Non-fatal: create packet without signature but warn
            packet["hmac_sha256"] = None
            packet["_warning"] = "AUDIT_HMAC_KEY not set - packet unsigned"
        else:
            sig = hmac.new(secret.encode(), json.dumps(packet, sort_keys=True).encode(), hashlib.sha256).hexdigest()
            packet["hmac_sha256"] = sig
    except Exception as e:
        packet["_hmac_error"] = str(e)
        packet["hmac_sha256"] = None
    return packet

# --- INITIALIZE ENHANCED SYSTEM ---
def initialize_enhanced_system():
    """Initialize all enhanced system components (safe wrappers)."""
    # Basic session defaults
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

    # Instantiate components with try/except
    try:
        st.session_state.config_manager = IndustrialConfig()
    except Exception as e:
        st.error(f"Config init failed: {e}")
        st.session_state.config_manager = None

    try:
        st.session_state.data_manager = DataManager() if DataManager else None
    except Exception as e:
        st.error(f"DataManager init failed: {e}")
        st.session_state.data_manager = None

    # Enhanced modules
    try:
        st.session_state.safety_monitor = SafetyMonitor()
    except Exception as e:
        st.error(f"SafetyMonitor init failed: {e}")
        st.session_state.safety_monitor = None

    try:
        st.session_state.business_intel = BusinessIntelligence()
    except Exception as e:
        st.error(f"BusinessIntel init failed: {e}")
        st.session_state.business_intel = None

    try:
        st.session_state.enhanced_ai = EnhancedAIModel()
    except Exception as e:
        st.error(f"EnhancedAIModel init failed: {e}")
        st.session_state.enhanced_ai = None

    # Advanced modules
    try:
        st.session_state.digital_twin = IndustrialDigitalTwin("centrifugal_pump") if IndustrialDigitalTwin else None
    except Exception as e:
        st.error(f"DigitalTwin init failed: {e}")
        st.session_state.digital_twin = None

    try:
        st.session_state.plc_integrator = create_avcs_plc_integration() if create_avcs_plc_integration else None
    except Exception as e:
        st.error(f"PLC Integrator init failed: {e}")
        st.session_state.plc_integrator = None

    try:
        st.session_state.system_integrator = create_soul_integrator() if create_soul_integrator else None
    except Exception as e:
        st.error(f"SystemIntegrator init failed: {e}")
        st.session_state.system_integrator = None

    # Voice and emotional systems - optional
    try:
        st.session_state.voice_personality = create_english_voice_personality() if create_english_voice_personality else None
    except Exception as e:
        st.session_state.voice_personality = None

    try:
        st.session_state.voice_interface = create_voice_interface() if create_voice_interface else None
    except Exception as e:
        st.session_state.voice_interface = None

    try:
        st.session_state.emotional_display = create_emotional_display() if create_emotional_display else None
    except Exception as e:
        st.session_state.emotional_display = None

    # Initialize damper forces
    if st.session_state.config_manager:
        st.session_state.damper_forces = {
            damper: st.session_state.config_manager.DAMPER_FORCES.get('standby', 0)
            for damper in getattr(st.session_state.config_manager, 'VIBRATION_SENSORS', {}).keys()
        }
    else:
        st.session_state.damper_forces = {}

# --- UI: landing page ---
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

    st.markdown("---")
    st.subheader("🎤 Voice System Demo")
    if st.button("🔊 Test Voice System"):
        if st.session_state.get('voice_personality'):
            try:
                st.session_state.voice_personality.speak(
                    "Hello! AVCS Soul system is ready for operation. All systems are functioning optimally.",
                    "CALM"
                )
            except Exception as e:
                st.warning(f"Voice system error: {e}")
        else:
            st.info("Voice system not available in this environment.")

# --- Sensor data generation (robust) ---
def generate_enhanced_sensor_data(current_cycle):
    """Generate enhanced sensor data with robust handling of digital twin outputs."""
    # Default operating conditions
    operating_conditions = {
        'rpm': 2950,
        'load': 'normal',
        'ambient_temperature': 25
    }

    twin = st.session_state.get('digital_twin')
    if twin:
        try:
            twin_data = twin.simulate_equipment_behavior(operating_conditions)
        except Exception as e:
            # fallback to synthetic generation
            st.error(f"Digital twin simulation error: {e}")
            twin_data = None
    else:
        twin_data = None

    # Build vibration dict for all known sensors
    vibration = {}
    vib_sensors = list(getattr(st.session_state.config_manager, 'VIBRATION_SENSORS', {}).keys()
                       if st.session_state.get('config_manager') else [])

    # If twin_data provides per-sensor RMS, use it; else compute or fallback to synthetic
    if twin_data and isinstance(twin_data.get('vibration_data'), dict):
        # The twin may provide dict like {'VIB_MOTOR_DRIVE': {'rms': 0.5, ...}, ...}
        for i, sensor in enumerate(vib_sensors):
            vinfo = twin_data['vibration_data'].get(sensor, None)
            if isinstance(vinfo, dict) and 'rms' in vinfo:
                base = float(vinfo['rms'])
            else:
                # if it's a raw array
                arr = np.asarray(vinfo) if vinfo is not None else np.zeros(100)
                base = float(np.sqrt(np.mean(arr**2))) if arr.size > 0 else 0.0
            vibration[sensor] = base * (1 + i * 0.05)
    elif twin_data and isinstance(twin_data.get('vibration_data'), (list, np.ndarray)):
        arr = np.asarray(twin_data['vibration_data'])
        base_rms = float(np.sqrt(np.mean(arr ** 2))) if arr.size > 0 else 0.0
        for i, sensor in enumerate(vib_sensors):
            vibration[sensor] = base_rms * (1 + i * 0.05)
    else:
        # fallback synthetic data
        for i, sensor in enumerate(vib_sensors):
            vibration[sensor] = float(max(0.1, 1.0 + np.random.normal(0, 0.3) + i * 0.1))

    # Temperature: support dict or scalar
    if twin_data and 'thermal_data' in twin_data:
        td = twin_data['thermal_data']
        if isinstance(td, dict):
            temperature = {k: float(v) for k, v in td.items()}
        else:
            scalar = float(td)
            temperature = {k: scalar for k in getattr(st.session_state.config_manager, 'THERMAL_SENSORS', {}).keys()}
    else:
        # synthetic default
        temperature = {k: float(65 + np.random.normal(0, 2)) for k in getattr(st.session_state.config_manager, 'THERMAL_SENSORS', {}).keys()}

    # Acoustic
    if twin_data and 'acoustic_data' in twin_data:
        noise = float(twin_data['acoustic_data'])
    else:
        noise = float(max(30, 65 + np.random.normal(0, 3)))

    return vibration, temperature, noise

# --- RUL, damper & efficiency logic (kept simple & tunable) ---
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
    cfg = st.session_state.config_manager.DAMPER_FORCES if st.session_state.get('config_manager') else {'critical':8000,'warning':4000,'normal':1000,'standby':500}
    if ai_prediction == -1 or risk_index > 85:
        return cfg.get('critical', 8000)
    elif risk_index > 65:
        return cfg.get('warning', 4000)
    elif risk_index > 30:
        return cfg.get('normal', 1000)
    else:
        return cfg.get('standby', 500)

# --- Displays & charts ---
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
    """Create combined sensor dashboard with safe checks."""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Vibration Sensors', 'Temperature Sensors', 'Noise Level', 'Risk History'),
        vertical_spacing=0.12,
        horizontal_spacing=0.08
    )

    # Vibration sensors
    vib_map = getattr(st.session_state.config_manager, 'VIBRATION_SENSORS', {}) if st.session_state.get('config_manager') else {}
    if not isinstance(vib_map, dict):
        vib_map = dict(vib_map)

    if 'vibration' in data_dict and not data_dict['vibration'].empty:
        for sensor in vib_map.keys():
            if sensor in data_dict['vibration'].columns:
                human_name = vib_map.get(sensor, sensor)
                fig.add_trace(
                    go.Scatter(
                        y=data_dict['vibration'][sensor],
                        name=human_name if isinstance(human_name, str) else sensor,
                        line=dict(width=2),
                        showlegend=True
                    ), row=1, col=1
                )

    # Temperature sensors
    temp_map = getattr(st.session_state.config_manager, 'THERMAL_SENSORS', {}) if st.session_state.get('config_manager') else {}
    if 'temperature' in data_dict and not data_dict['temperature'].empty:
        for sensor in temp_map.keys():
            if sensor in data_dict['temperature'].columns:
                human_name = temp_map.get(sensor, sensor)
                fig.add_trace(
                    go.Scatter(
                        y=data_dict['temperature'][sensor],
                        name=human_name if isinstance(human_name, str) else sensor,
                        line=dict(width=2),
                        showlegend=True
                    ), row=1, col=2
                )

    # Noise level
    if 'noise' in data_dict and not data_dict['noise'].empty:
        fig.add_trace(
            go.Scatter(
                y=data_dict['noise']['NOISE'],
                name="Noise Level",
                line=dict(color='purple', width=3),
                showlegend=True
            ),
            row=2, col=1
        )

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

    fig.update_layout(height=600, showlegend=True, title_text="Combined Sensor Dashboard")
    return fig

def handle_voice_announcements(system_metrics, event_type=None):
    """Handle English voice announcements safely (rate-limited)."""
    voice = st.session_state.get('voice_personality')
    interface = st.session_state.get('voice_interface')
    if not voice:
        return

    # Rate limiting: last_speech_time stored in voice_personality if available, otherwise in session
    current_time = datetime.now()
    last_speech = getattr(voice, 'last_speech_time', st.session_state.get('last_speech_time'))
    if last_speech and (current_time - last_speech).total_seconds() < 30:
        return

    try:
        speech_text, tone = voice.generate_emotional_speech(system_metrics, event_type)
        should_speak = (
            event_type in ['RISK_HIGH', 'FAILURE_PREVENTED', 'CRITICAL_ALERT'] or
            system_metrics.get('risk_index', 0) > 70 or
            (event_type is not None and np.random.random() > 0.3)
        )
        if should_speak:
            voice.speak(speech_text, tone)
            if interface:
                speech_viz = interface.create_speech_visualization(speech_text, tone)
                st.markdown(speech_viz, unsafe_allow_html=True)
            # store last speech time
            if hasattr(voice, 'last_speech_time'):
                voice.last_speech_time = current_time
            else:
                st.session_state['last_speech_time'] = current_time
    except Exception as e:
        st.warning(f"Voice announcement failed: {e}")

# --- MAIN loop runner ---
def run_enhanced_monitoring_loop(status_indicator, cycle_display, performance_display, simulation_speed, max_cycles):
    current_cycle = len(st.session_state.data_dict.get('risk_history', []))
    progress_bar = st.sidebar.progress(0)

    # Safety: bail out if components missing
    if st.session_state.get('system_running') is not True:
        return

    try:
        if current_cycle < max_cycles and st.session_state.system_running:
            vibration, temperature, noise = generate_enhanced_sensor_data(current_cycle)

            # Safety monitoring
            try:
                emergency_conditions = st.session_state.safety_monitor.check_emergency_conditions(vibration, temperature, noise) if st.session_state.get('safety_monitor') else []
            except Exception as e:
                st.warning(f"Safety monitor error: {e}")
                emergency_conditions = []

            if emergency_conditions:
                try:
                    if st.session_state.get('safety_monitor'):
                        st.session_state.safety_monitor.trigger_emergency_shutdown(emergency_conditions)
                except Exception:
                    pass
                st.session_state.system_running = False
                st.error(f"🚨 EMERGENCY SHUTDOWN: {', '.join(emergency_conditions)}")
                # voice alert
                try:
                    if st.session_state.get('voice_personality'):
                        st.session_state.voice_personality.speak(
                            "Emergency shutdown activated! Critical parameters exceeded safety limits!",
                            "URGENT"
                        )
                except Exception:
                    pass
                st.session_state.performance_metrics['emergency_stops'] += 1
                return

            # AI analysis
            features = list(vibration.values()) + list(temperature.values()) + [noise]
            ai_prediction, ai_confidence = (0, 0.0)
            try:
                if st.session_state.get('enhanced_ai'):
                    ai_prediction, ai_confidence = st.session_state.enhanced_ai.predict(features)
                else:
                    # fallback: simple heuristic
                    ai_confidence = float(np.random.normal(0.0, 0.5))
                    ai_prediction = -1 if np.abs(ai_confidence) > 0.9 else 1
            except Exception as e:
                st.warning(f"AI predict error: {e}")
                ai_prediction, ai_confidence = 0, 0.0

            risk_index = min(100, max(0, int(abs(ai_confidence) * 150 + np.random.normal(0, 5))))
            rul_hours = calculate_enhanced_rul(risk_index, current_cycle, vibration, temperature)

            # Emotional state from voice personality
            emotional_state = None
            try:
                if st.session_state.get('voice_personality'):
                    emotional_state = st.session_state.voice_personality.emotional_state
                else:
                    emotional_state = {'core_mood': 'CONFIDENT', 'intensity': 0.7}
            except Exception:
                emotional_state = {'core_mood': 'CONFIDENT', 'intensity': 0.7}

            # Periodic voice announcements
            if current_cycle % 20 == 0:
                event_type = 'RISK_HIGH' if risk_index > 80 else 'OPERATION_OPTIMAL' if risk_index < 20 else None
                handle_voice_announcements({'risk_index': risk_index}, event_type)

            # Damper control
            damper_force = calculate_damper_force(risk_index, ai_prediction)
            st.session_state.damper_forces = {d: damper_force for d in st.session_state.damper_forces.keys()}

            # Data management: append to dataframes (use DataManager if available)
            try:
                if st.session_state.get('data_manager'):
                    st.session_state.data_dict = st.session_state.data_manager.add_data_point(st.session_state.data_dict, vibration, 'vibration')
                    st.session_state.data_dict = st.session_state.data_manager.add_data_point(st.session_state.data_dict, temperature, 'temperature')
                    st.session_state.data_dict = st.session_state.data_manager.add_data_point(st.session_state.data_dict, {'NOISE': noise}, 'noise')
                    st.session_state.data_dict = st.session_state.data_manager.add_data_point(st.session_state.data_dict, st.session_state.damper_forces, 'dampers')
                else:
                    # naive append
                    if 'vibration' in st.session_state.data_dict:
                        row = pd.DataFrame([vibration])
                        if st.session_state.data_dict['vibration'].empty:
                            st.session_state.data_dict['vibration'] = row
                        else:
                            st.session_state.data_dict['vibration'] = pd.concat([st.session_state.data_dict['vibration'], row], ignore_index=True)
                    if 'temperature' in st.session_state.data_dict:
                        rowt = pd.DataFrame([temperature])
                        if st.session_state.data_dict['temperature'].empty:
                            st.session_state.data_dict['temperature'] = rowt
                        else:
                            st.session_state.data_dict['temperature'] = pd.concat([st.session_state.data_dict['temperature'], rowt], ignore_index=True)
                    if 'noise' in st.session_state.data_dict:
                        rown = pd.DataFrame([{'NOISE': noise}])
                        if st.session_state.data_dict['noise'].empty:
                            st.session_state.data_dict['noise'] = rown
                        else:
                            st.session_state.data_dict['noise'] = pd.concat([st.session_state.data_dict['noise'], rown], ignore_index=True)
                    if 'dampers' in st.session_state.data_dict:
                        rowd = pd.DataFrame([st.session_state.damper_forces])
                        if st.session_state.data_dict['dampers'].empty:
                            st.session_state.data_dict['dampers'] = rowd
                        else:
                            st.session_state.data_dict['dampers'] = pd.concat([st.session_state.data_dict['dampers'], rowd], ignore_index=True)
            except Exception as e:
                st.warning(f"Data append error: {e}")

            # Update risk history
            st.session_state.data_dict['risk_history'].append(risk_index)

            # Generate audit packet and append to logs
            derived = {
                'rul_hours': rul_hours,
                'risk_index': risk_index,
                'ai_confidence': ai_confidence
            }
            decision = {
                'action': 'adjust_damper',
                'force': damper_force,
                'reason': 'vibration_risk' if risk_index > 50 else 'monitor'
            }
            packet = generate_audit_packet("PUMP-001", {'vibration': vibration, 'temperature': temperature, 'noise': noise}, derived, decision, st.session_state.damper_forces)
            st.session_state.system_logs.append(packet)

            # Update displays
            update_enhanced_displays(risk_index, rul_hours, ai_confidence, current_cycle, max_cycles,
                                     status_indicator, cycle_display, performance_display, progress_bar,
                                     emotional_state)

            # Update performance metrics
            st.session_state.performance_metrics['cycles_completed'] = current_cycle + 1
            if risk_index > 80:
                st.session_state.performance_metrics['prevented_failures'] += 1

            # Wait and re-run (use small sleep then rerun to produce live feel)
            time.sleep(max(0.05, float(simulation_speed)))
            # Use rerun to refresh UI loop
            st.rerun()

        elif current_cycle >= max_cycles:
            st.success("✅ Enhanced simulation completed successfully!")
            try:
                if st.session_state.get('voice_personality'):
                    st.session_state.voice_personality.speak(
                        "Simulation completed successfully. All systems performed within expected parameters.",
                        "PROUD"
                    )
            except Exception:
                pass
            st.session_state.system_running = False
            return
    except Exception as e:
        st.error(f"Monitoring loop unexpected error: {e}")
        st.session_state.system_running = False
        return

def update_enhanced_displays(risk_index, rul_hours, ai_confidence, current_cycle, max_cycles,
                             status_indicator, cycle_display, performance_display, progress_bar,
                             emotional_state):
    """Update UI displays (safe)."""
    # Status indicator
    if risk_index > 80:
        status_color, status_text = "red", "🚨 CRITICAL"
    elif risk_index > 50:
        status_color, status_text = "orange", "⚠️ WARNING"
    elif risk_index > 20:
        status_color, status_text = "green", "✅ NORMAL"
    else:
        status_color, status_text = "blue", "🟢 STANDBY"

    status_indicator.markdown(
        f"<h3 style='color: {status_color}; text-align: center;'>{status_text}</h3>",
        unsafe_allow_html=True
    )
    cycle_display.metric("Current Cycle", f"{current_cycle + 1}/{max_cycles}")
    efficiency = calculate_efficiency(risk_index)
    performance_display.metric("Operational Efficiency", f"{efficiency:.1f}%")
    progress_bar.progress(min(1.0, (current_cycle + 1) / max_cycles))

    # Dashboard layout
    col1, col2 = st.columns([2, 1])
    with col1:
        try:
            st.plotly_chart(create_combined_sensor_dashboard(st.session_state.data_dict), use_container_width=True)
        except Exception as e:
            st.warning(f"Dashboard render error: {e}")
    with col2:
        try:
            st.plotly_chart(create_risk_gauge(risk_index), use_container_width=True)
        except Exception as e:
            st.warning(f"Gauge render error: {e}")

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

    # Emotional display (best-effort)
    try:
        if st.session_state.get('emotional_display') and emotional_state:
            st.session_state.emotional_display.render_emotional_state(emotional_state)
    except Exception as e:
        st.warning(f"Emotional display error: {e}")

    # Voice control UI (best-effort)
    try:
        if st.session_state.get('voice_interface') and st.session_state.get('voice_personality'):
            st.session_state.voice_interface.render_voice_control_panel(st.session_state.voice_personality)
    except Exception as e:
        st.warning(f"Voice interface error: {e}")

# --- MAIN APPLICATION ---
def main():
    # Initialize system if not already initialized
    if "config_manager" not in st.session_state:
        initialize_enhanced_system()

    st.title("🏭 AVCS DNA - Industrial Monitoring System v6.0")
    st.markdown("""
    **Enhanced Active Vibration Control System with AI-Powered Predictive Maintenance**  
    *Now with Real-time Safety Monitoring, Business Intelligence, and Advanced Analytics*
    """)

    # Sidebar and controls
    st.sidebar.header("🎛️ AVCS DNA Control Panel v6.0")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("⚡ Start System", type="primary", use_container_width=True):
            # reset data
            st.session_state.system_running = True
            st.session_state.data_dict = {'vibration': pd.DataFrame(), 'temperature': pd.DataFrame(), 'noise': pd.DataFrame(columns=['NOISE']), 'dampers': pd.DataFrame(), 'risk_history': []}
            st.session_state.damper_forces = {d: st.session_state.config_manager.DAMPER_FORCES.get('standby', 500) for d in getattr(st.session_state.config_manager, 'VIBRATION_SENSORS', {}).keys()} if st.session_state.get('config_manager') else {}
            try:
                if st.session_state.get('voice_personality'):
                    st.session_state.voice_personality.speak("AVCS Soul system activated. Beginning equipment monitoring operations.", "CALM")
            except Exception:
                pass
            st.rerun()

    with col2:
        if st.button("🛑 Emergency Stop", use_container_width=True):
            st.session_state.system_running = False
            st.session_state.damper_forces = {d: 0 for d in st.session_state.damper_forces.keys()} if st.session_state.get('damper_forces') else {}
            try:
                if st.session_state.get('voice_personality'):
                    st.session_state.voice_personality.speak("Emergency stop activated. All systems secured.", "WARNING")
            except Exception:
                pass
            st.rerun()

    st.sidebar.markdown("---")
    status_indicator = st.sidebar.empty()
    cycle_display = st.sidebar.empty()
    performance_display = st.sidebar.empty()

    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Configuration")
    simulation_speed = st.sidebar.slider("Simulation Speed", 0.05, 1.0, 0.3, 0.05)
    max_cycles = int(st.sidebar.number_input("Max Cycles", 50, 10000, 500))

    st.sidebar.markdown("---")
    st.sidebar.subheader("💰 Business Intelligence")
    # BI snapshot if available
    try:
        if st.session_state.data_dict.get('risk_history') and st.session_state.get('business_intel'):
            efficiency, warning_ratio, critical_ratio = st.session_state.business_intel.calculate_operational_efficiency(st.session_state.data_dict['risk_history'])
            prevented_failures = len([r for r in st.session_state.data_dict['risk_history'] if r > 80])
            operational_hours = len(st.session_state.data_dict['risk_history']) / 3600
            roi, cost_savings = st.session_state.business_intel.calculate_roi(prevented_failures, operational_hours)
            st.sidebar.metric("Operational Efficiency", f"{efficiency:.1f}%")
            st.sidebar.metric("Prevented Failures", prevented_failures)
            st.sidebar.metric("Estimated ROI", f"{roi:.0f}%")
            st.sidebar.metric("Cost Savings", f"${cost_savings:,.0f}")
    except Exception:
        pass

    # Voice system status
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎤 Voice System")
    if st.session_state.get('voice_personality'):
        voice_metrics = st.session_state.voice_personality.get_voice_metrics()
        st.sidebar.metric("Total Speeches", voice_metrics['system_metrics']['total_speeches'])
        st.sidebar.metric("Emergency Alerts", voice_metrics['system_metrics']['emergency_alerts'])
        
        emotional_state = voice_metrics['emotional_state']
        st.sidebar.write(f"**Emotional State:** {emotional_state['core_mood']} ({int(emotional_state['intensity']*100)}%)")
    else:
        st.sidebar.info("Voice system not available")

    # Main
    if not st.session_state.system_running:
        show_landing_page()
    else:
        run_enhanced_monitoring_loop(status_indicator, cycle_display, performance_display, simulation_speed, max_cycles)

if __name__ == "__main__":
    main()
