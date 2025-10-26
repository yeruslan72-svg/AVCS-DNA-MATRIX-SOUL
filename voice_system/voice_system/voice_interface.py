# voice_interface.py - Enhanced English Voice Interface
import streamlit as st
from datetime import datetime

class EnglishVoiceInterface:
    """Enhanced English voice interface control panel with emotional intelligence"""
    
    def render_voice_control_panel(self, voice_personality):
        """Render enhanced English voice control panel"""
        
        st.markdown("---")
        st.subheader("🎤 AVCS Soul Voice System (English)")
        
        # Voice metrics display
        self.render_voice_metrics(voice_personality)
        
        # Main control columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            self.render_voice_controls(voice_personality)
            
        with col2:
            self.render_alert_settings(voice_personality)
            
        with col3:
            self.render_voice_activity(voice_personality)
        
        # Quick messages and demonstrations
        self.render_quick_messages(voice_personality)
        self.render_demonstration_phrases(voice_personality)
        
        # Voice history
        self.render_voice_history(voice_personality)
    
    def render_voice_metrics(self, voice_personality):
        """Render voice system metrics"""
        metrics = voice_personality.get_voice_metrics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Speeches", metrics['system_metrics']['total_speeches'])
        with col2:
            st.metric("Emergency Alerts", metrics['system_metrics']['emergency_alerts'])
        with col3:
            st.metric("Failures Prevented", metrics['system_metrics']['prevented_failures'])
        with col4:
            st.metric("Today's Messages", metrics['total_speeches_today'])
    
    def render_voice_controls(self, voice_personality):
        """Render voice control buttons"""
        st.write("**🎛️ Voice Control:**")
        
        if st.button("🔊 Test Voice System", key="voice_test_en", use_container_width=True):
            voice_personality.speak("Voice system activated and ready for operation!", "CALM")
            
        if st.button("🤖 System Status Report", key="system_status_en", use_container_width=True):
            voice_personality.speak("Checking current system status... All parameters are optimal.", "CALM")
            
        if st.button("❤️ Emotional Status", key="emotional_check", use_container_width=True):
            emotional_state = voice_personality.emotional_state
            message = f"I'm feeling {emotional_state['core_mood'].lower()} with {int(emotional_state['intensity']*100)}% intensity today!"
            voice_personality.speak(message, "EXCITED")
            
        if st.button("🔄 Update Metrics", key="update_metrics", use_container_width=True):
            st.rerun()
    
    def render_alert_settings(self, voice_personality):
        """Render alert settings panel"""
        st.write("**⚙️ Alert Settings:**")
        
        voice_alert_level = st.selectbox(
            "Voice Alert Level",
            ["Critical Only", "Important & Critical", "All Events", "Verbose"],
            key="alert_level_en"
        )
        
        auto_speech = st.checkbox("Automatic System Announcements", value=True, key="auto_speech_en")
        emergency_override = st.checkbox("Emergency Message Priority", value=True, key="emergency_override")
        
        st.write("**🎭 Voice Personality:**")
        voice_style = st.selectbox(
            "Speaking Style",
            ["Professional", "Friendly", "Technical", "Emotional", "Concise"],
            key="voice_style"
        )
    
    def render_voice_activity(self, voice_personality):
        """Render voice activity status"""
        st.write("**📊 Voice Activity:**")
        
        metrics = voice_personality.get_voice_metrics()
        
        if voice_personality.is_speaking:
            st.error("🔴 SYSTEM SPEAKING")
            st.write("Current message in progress...")
            st.progress(70)  # Simulated progress
        else:
            st.success("🟢 READY TO SPEAK")
            st.write("Voice system standing by")
            
        if voice_personality.last_speech_time:
            time_diff = datetime.now() - voice_personality.last_speech_time
            minutes_ago = int(time_diff.total_seconds() / 60)
            st.caption(f"Last speech: {minutes_ago} minutes ago")
        
        # Emotional state display
        emotional_state = voice_personality.emotional_state
        emotion_emoji = {
            'CONFIDENT': '😊', 'PROUD': '🏆', 'CONTENT': '😌', 
            'CONCERNED': '😟', 'ANXIOUS': '😰', 'EXCITED': '🎉'
        }
        
        st.write(f"**{emotion_emoji.get(emotional_state['core_mood'], '😐')} Emotional State:**")
        st.write(f"{emotional_state['core_mood']} ({int(emotional_state['intensity']*100)}%)")
        st.progress(emotional_state['intensity'])
    
    def render_quick_messages(self, voice_personality):
        """Render quick message buttons"""
        st.write("**🚀 Quick Messages:**")
        quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)
        
        with quick_col1:
            if st.button("🚨 Emergency Alert", key="alert_btn_en", use_container_width=True):
                alert_data = {
                    'type': 'VIBRATION_CRITICAL',
                    'severity': 'HIGH',
                    'location': 'Motor Drive End',
                    'value': '7.2 mm/s'
                }
                voice_personality.handle_system_alert(alert_data)
                
        with quick_col2:
            if st.button("✅ All Systems Normal", key="ok_btn_en", use_container_width=True):
                alert_data = {
                    'type': 'SYSTEM_OPTIMAL',
                    'severity': 'LOW', 
                    'location': 'All Equipment',
                    'value': '96%'
                }
                voice_personality.handle_system_alert(alert_data)
                
        with quick_col3:
            if st.button("📊 Performance Report", key="report_btn_en", use_container_width=True):
                voice_personality.speak("Generating comprehensive performance report. Overall system efficiency is ninety-four percent with optimal vibration control.", "PROUD")
                
        with quick_col4:
            if st.button("🔇 Mute Announcements", key="mute_btn_en", use_container_width=True):
                voice_personality.speak("Voice announcements temporarily disabled. Silent monitoring mode activated.", "CALM")
    
    def render_demonstration_phrases(self, voice_personality):
        """Render demonstration phrase buttons"""
        st.write("**🎭 Demonstration Phrases:**")
        demo_col1, demo_col2, demo_col3, demo_col4 = st.columns(4)
        
        with demo_col1:
            if st.button("😊 Happy Message", key="happy_demo", use_container_width=True):
                voice_personality.speak("I'm absolutely delighted with our system performance today! Everything is running with exceptional efficiency!", "EXCITED")
                
        with demo_col2:
            if st.button("😟 Concerned Alert", key="concerned_demo", use_container_width=True):
                voice_personality.speak("I'm detecting concerning vibration patterns that require immediate attention. Recommend detailed inspection of the motor bearings.", "WARNING")
                
        with demo_col3:
            if st.button("🎉 Success Story", key="success_demo", use_container_width=True):
                voice_personality.speak("Outstanding success! My predictive algorithms just prevented a catastrophic equipment failure! Teamwork makes the dream work!", "PROUD")
                
        with demo_col4:
            if st.button("🔧 Maintenance", key="maintenance_demo", use_container_width=True):
                voice_personality.speak("Preventive maintenance alert. Based on operational data, recommend scheduling service for the pump assembly within the next 48 hours.", "CALM")
    
    def render_voice_history(self, voice_personality):
        """Render voice history panel"""
        metrics = voice_personality.get_voice_metrics()
        
        if metrics['recent_activity']:
            st.write("**📝 Recent Voice Activity:**")
            
            for i, speech in enumerate(reversed(metrics['recent_activity'])):
                with st.expander(f"🎤 {speech['timestamp'].strftime('%H:%M:%S')} - {speech['tone']}", expanded=i==0):
                    st.write(f"**Message:** {speech['text']}")
                    col1, col2, col3 = st.columns([2,1,1])
                    with col1:
                        st.write(f"**Tone:** {speech['tone']}")
                    with col2:
                        st.write(f"**Priority:** {speech['priority']}")
                    with col3:
                        if st.button(f"Replay", key=f"replay_{i}"):
                            voice_personality.speak(speech['text'], speech['tone'])
                    
                    # Display speech visualization
                    st.markdown(self.create_speech_visualization(speech['text'], speech['tone']), unsafe_allow_html=True)
    
    def create_speech_visualization(self, text, tone):
        """Create enhanced speech visualization"""
        tone_colors = {
            'CALM': '#42A5F5',
            'WARNING': '#FFA726', 
            'URGENT': '#EF5350',
            'PROUD': '#AB47BC',
            'EXCITED': '#66BB6A'
        }
        
        tone_icons = {
            'CALM': '🔵',
            'WARNING': '🟠',
            'URGENT': '🔴', 
            'PROUD': '🟣',
            'EXCITED': '🟢'
        }
        
        return f"""
        <div style="background: linear-gradient(90deg, {tone_colors.get(tone, '#667eea')} 0%, #764ba2 100%); 
                    padding: 12px; border-radius: 10px; color: white; text-align: center;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: 10px 0;">
            {tone_icons.get(tone, '🎤')} <strong>SYSTEM SPEAKING:</strong> "{text}"
            <br><small>Tone: {tone} • {datetime.now().strftime('%H:%M:%S')}</small>
        </div>
        """

# Factory function for easy instantiation
def create_voice_interface():
    """Create and initialize voice interface"""
    return EnglishVoiceInterface()
