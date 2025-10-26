# --- VOICE SYSTEM ---
class EnglishVoicePersonality:
    def __init__(self):
        self.last_speech_time = None
        self.emotional_state = {'core_mood': 'CONFIDENT', 'intensity': 0.7}
        
    def generate_emotional_speech(self, system_metrics, event_type):
        risk_index = system_metrics.get('risk_index', 0)
        rul_hours = system_metrics.get('rul_hours', 100)
        
        if event_type == 'RISK_HIGH' or risk_index > 80:
            return "Warning! System risk level critical. Immediate attention recommended.", "URGENT"
        elif event_type == 'FAILURE_PREVENTED':
            return "Excellent! Potential failure has been prevented. System stability restored.", "PROUD"
        elif risk_index > 50:
            return "Caution. System parameters approaching warning thresholds. Monitoring closely.", "ALERT"
        elif rul_hours < 24:
            return "Remaining useful life critically low. Schedule maintenance immediately.", "CONCERNED"
        else:
            return "All systems operating within normal parameters. Performance optimal.", "CALM"
    
    def speak(self, text, tone):
        # In real implementation, this would use TTS
        print(f"🔊 VOICE [{tone}]: {text}")
        self.last_speech_time = datetime.now()

class VoiceInterface:
    def create_speech_visualization(self, text, tone):
        tone_colors = {
            'URGENT': '🔴',
            'ALERT': '🟡', 
            'CALM': '🟢',
            'PROUD': '🔵',
            'CONCERNED': '🟠'
        }
        return f"""
        <div style="background: #f0f8ff; padding: 15px; border-radius: 10px; border-left: 5px solid #4CAF50; margin: 10px 0;">
            <div style="display: flex; align-items: center; gap: 10px;">
                {tone_colors.get(tone, '🔊')}
                <strong style="color: #333;">AI Voice:</strong>
            </div>
            <p style="margin: 10px 0 0 0; color: #555; font-style: italic;">"{text}"</p>
            <div style="font-size: 12px; color: #888; margin-top: 5px;">Tone: {tone}</div>
        </div>
        """

# --- EMOTIONAL DISPLAY ---
class EmotionalDisplay:
    def render_emotional_state(self, emotional_state):
        mood = emotional_state.get('core_mood', 'NEUTRAL')
        intensity = emotional_state.get('intensity', 0.5)
        
        mood_emojis = {
            'CONFIDENT': '😊', 'ALERT': '👁️', 'URGENT': '🚨',
            'CALM': '😌', 'PROUD': '🦸', 'CONCERNED': '😟'
        }
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("🧠 AI Emotional State")
        st.sidebar.write(f"{mood_emojis.get(mood, '🤖')} **{mood}**")
        st.sidebar.progress(intensity)

# --- ОБНОВЛЕННАЯ ИНИЦИАЛИЗАЦИЯ ---
def initialize_enhanced_system():
    # ... предыдущий код инициализации ...
    
    # Добавляем голосовую систему
    st.session_state.voice_personality = EnglishVoicePersonality()
    st.session_state.voice_interface = VoiceInterface()
    st.session_state.emotional_display = EmotionalDisplay()

# --- ОБНОВЛЕННЫЙ МОНИТОРИНГ С ГОЛОСОМ ---
def handle_voice_announcements(system_metrics, event_type=None):
    """Обработка голосовых объявлений"""
    voice = st.session_state.get('voice_personality')
    interface = st.session_state.get('voice_interface')
    
    if not voice:
        return

    # Ограничение частоты сообщений
    current_time = datetime.now()
    if voice.last_speech_time and (current_time - voice.last_speech_time).total_seconds() < 30:
        return

    try:
        speech_text, tone = voice.generate_emotional_speech(system_metrics, event_type)
        
        # Условия для голосовых сообщений
        should_speak = (
            event_type in ['RISK_HIGH', 'FAILURE_PREVENTED', 'CRITICAL_ALERT'] or
            system_metrics.get('risk_index', 0) > 70 or
            (event_type is not None and np.random.random() > 0.3)
        )
        
        if should_speak:
            # Голосовое сообщение
            voice.speak(speech_text, tone)
            
            # Визуализация в интерфейсе
            if interface:
                speech_viz = interface.create_speech_visualization(speech_text, tone)
                st.markdown(speech_viz, unsafe_allow_html=True)
            
            voice.last_speech_time = current_time
            
    except Exception as e:
        st.warning(f"Voice announcement failed: {e}")

# --- ОБНОВЛЕННЫЙ МОНИТОРИНГ С ГОЛОСОВЫМИ СОБЫТИЯМИ ---
def run_enhanced_monitoring_loop(status_indicator, cycle_display, performance_display, simulation_speed, max_cycles):
    # ... предыдущий код ...
    
    if current_cycle < max_cycles and st.session_state.system_running:
        # ... генерация данных и анализ ...
        
        # ГОЛОСОВЫЕ УВЕДОМЛЕНИЯ
        system_metrics = {
            'risk_index': risk_index,
            'rul_hours': rul_hours,
            'vibration': max(vibration.values()) if vibration else 0,
            'temperature': max(temperature.values()) if temperature else 0,
            'noise': noise
        }
        
        # Определяем тип события для голосового уведомления
        event_type = None
        if risk_index > 85:
            event_type = 'CRITICAL_ALERT'
        elif risk_index > 70:
            event_type = 'RISK_HIGH'
        elif any(cond for cond in emergency_conditions if "CRITICAL" in cond):
            event_type = 'EMERGENCY_SHUTDOWN'
        
        # Периодические сообщения каждые 20 циклов
        if current_cycle % 20 == 0:
            event_type = 'STATUS_UPDATE'
        
        # Запускаем голосовое уведомление
        handle_voice_announcements(system_metrics, event_type)
        
        # Обновляем эмоциональное состояние
        emotional_state = st.session_state.voice_personality.emotional_state
        if risk_index > 70:
            emotional_state = {'core_mood': 'URGENT', 'intensity': 0.9}
        elif risk_index > 50:
            emotional_state = {'core_mood': 'ALERT', 'intensity': 0.7}
        else:
            emotional_state = {'core_mood': 'CONFIDENT', 'intensity': 0.6}
        
        st.session_state.voice_personality.emotional_state = emotional_state

# --- ГОЛОСОВОЕ УПРАВЛЕНИЕ В САЙДБАРЕ ---
def add_voice_control_panel():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎤 Voice Control")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("🔊 Test Voice", use_container_width=True):
            test_metrics = {'risk_index': 30, 'rul_hours': 150}
            handle_voice_announcements(test_metrics, 'STATUS_UPDATE')
    
    with col2:
        if st.button("📢 Emergency", use_container_width=True):
            emergency_metrics = {'risk_index': 90, 'rul_hours': 5}
            handle_voice_announcements(emergency_metrics, 'CRITICAL_ALERT')
    
    # Ручное голосовое сообщение
    voice_message = st.sidebar.text_input("Custom message:")
    if st.sidebar.button("Send Custom", use_container_width=True) and voice_message:
        st.session_state.voice_personality.speak(voice_message, "CALM")

# --- ОБНОВЛЕННАЯ MAIN FUNCTION ---
def main():
    # ... предыдущий код main ...
    
    # Добавляем панель голосового управления в сайдбар
    add_voice_control_panel()
    
    # Добавляем эмоциональное состояние
    if st.session_state.get('emotional_display') and st.session_state.get('voice_personality'):
        st.session_state.emotional_display.render_emotional_state(
            st.session_state.voice_personality.emotional_state
        )
