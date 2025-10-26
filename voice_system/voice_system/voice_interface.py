# voice_interface.py - English Voice Interface
import streamlit as st
from datetime import datetime

class EnglishVoiceInterface:
    """English voice interface control panel"""
    
    def render_voice_control_panel(self, voice_personality):
        """Render English voice control panel"""
        
        st.markdown("---")
        st.subheader("🎤 AVCS Soul Voice System (English)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Voice Control:**")
            
            if st.button("🔊 Test Voice", key="voice_test_en"):
                voice_personality.speak("Voice system activated and ready for operation!", "CALM")
                
            if st.button("🤖 System Status", key="system_status_en"):
                voice_personality.speak("Checking current system status... All parameters are optimal.", "CALM")
                
            if st.button("❤️ Emotional Check", key="emotional_check"):
                voice_personality.speak("I'm feeling confident and ready to protect your equipment today!", "EXCITED")
                
        with col2:
            st.write("**Alert Settings:**")
            
            voice_alert_level = st.selectbox(
                "Voice Alert Level",
                ["Critical Only", "Important & Critical", "All Events"],
                key="alert_level_en"
            )
            
            auto_speech = st.checkbox("Automatic Announcements", value=True, key="auto_speech_en")
            
            st.write("**Voice Personality:**")
            voice_style = st.selectbox(
                "Speaking Style",
                ["Professional", "Friendly", "Technical", "Emotional"],
                key="voice_style"
            )
            
        with col3:
            st.write("**Voice Activity:**")
            
            if voice_personality.is_speaking:
                st.error("🔴 SYSTEM SPEAKING")
                st.write("Please wait for current message to complete...")
            else:
                st.success("🟢 READY TO SPEAK")
                
            if voice_personality.last_speech_time:
                st.caption(f"Last speech: {voice_personality.last_speech_time.strftime('%H:%M:%S')}")
            
            st.metric("Messages Today", "12")
            st.metric("Voice Uptime", "99.8%")
        
        # Quick message buttons
        st.write("**Quick Messages:**")
        quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)
        
        with quick_col1:
            if st.button("🚨 Emergency Alert", key="alert_btn_en"):
                voice_personality.speak("Attention! Emergency protocol activated! Immediate action required!", "URGENT")
                
        with quick_col2:
            if st.button("✅ All Systems Normal", key="ok_btn_en"):
                voice_personality.speak("All systems operating within normal parameters. Continuing monitoring operations.", "CALM")
                
        with quick_col3:
            if st.button("📊 Performance Report", key="report_btn_en"):
                voice_personality.speak("Generating verbal performance report. Current efficiency is ninety-four percent.", "PROUD")
                
        with quick_col4:
            if st.button("🔇 Mute Voice", key="mute_btn_en"):
                voice_personality.speak("Voice announcements temporarily disabled. Silent mode activated.", "CALM")
        
        # Demonstration phrases
        st.write("**Demonstration Phrases:**")
        demo_col1, demo_col2, demo_col3 = st.columns(3)
        
        with demo_col1:
            if st.button("😊 Happy Message", key="happy_demo"):
                voice_personality.speak("I'm so happy with our system performance today! Everything is running perfectly!", "EXCITED")
                
        with demo_col2:
            if st.button("😟 Concerned Message", key="concerned_demo"):
                voice_personality.speak("I'm concerned about the vibration patterns I'm detecting. We should investigate this further.", "WARNING")
                
        with demo_col3:
            if st.button("🎉 Success Story", key="success_demo"):
                voice_personality.speak("We did it! My predictive algorithms just prevented a potential equipment failure! I'm so proud!", "PROUD")
    
    def create_speech_visualization(self, text, tone):
        """Create speech visualization"""
        tone_colors = {
            'CALM': '#42A5F5',
            'WARNING': '#FFA726',
            'URGENT': '#EF5350',
            'PROUD': '#AB47BC',
            'EXCITED': '#66BB6A'
        }
        
        return f"""
        <div style="background: linear-gradient(90deg, {tone_colors.get(tone, '#667eea')} 0%, #764ba2 100%); 
                    padding: 12px; border-radius: 10px; color: white; text-align: center;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: 10px 0;">
            🎤 <strong>SYSTEM SPEAKING:</strong> "{text}"
            <br><small>Tone: {tone} • {datetime.now().strftime('%H:%M:%S')}</small>
        </div>
        """
