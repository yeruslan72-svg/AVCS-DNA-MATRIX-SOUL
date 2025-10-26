# emotional_display.py - Emotional State Visualization
import streamlit as st
from datetime import datetime

class EmotionalDisplay:
    """Emotional state visualization for AVCS Soul"""
    
    def __init__(self):
        self.emotion_colors = {
            'CONFIDENT': '#4CAF50',
            'PROUD': '#9C27B0', 
            'CONTENT': '#2196F3',
            'CONCERNED': '#FF9800',
            'ANXIOUS': '#F44336',
            'EXCITED': '#FFEB3B'
        }
        
        self.emotion_emojis = {
            'CONFIDENT': '😊',
            'PROUD': '🏆',
            'CONTENT': '😌',
            'CONCERNED': '😟', 
            'ANXIOUS': '😰',
            'EXCITED': '🎉'
        }
    
    def render_emotional_state(self, emotional_state):
        """Render emotional state visualization"""
        st.subheader("❤️ Emotional State")
        
        emotion = emotional_state['core_mood']
        intensity = emotional_state['intensity']
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Emotion emoji and name
            st.markdown(f"### {self.emotion_emojis.get(emotion, '😐')} {emotion}")
            st.metric("Intensity", f"{int(intensity * 100)}%")
            
            # Last update
            if 'last_update' in emotional_state:
                last_update = emotional_state['last_update']
                if isinstance(last_update, str):
                    st.caption(f"Last update: {last_update}")
                else:
                    st.caption(f"Last update: {last_update.strftime('%H:%M:%S')}")
        
        with col2:
            # Intensity progress bar
            st.progress(intensity)
            
            # Color-coded emotion indicator
            color = self.emotion_colors.get(emotion, '#666666')
            st.markdown(
                f"""<div style="background: {color}; padding: 10px; border-radius: 5px; color: white; text-align: center;">
                    Current Emotional State
                </div>""", 
                unsafe_allow_html=True
            )
    
    def render_emotional_timeline(self, speech_history):
        """Render emotional timeline from speech history"""
        if not speech_history or len(speech_history) < 2:
            return
            
        st.write("**📈 Emotional Timeline:**")
        
        # Get recent emotional states
        recent_states = []
        for speech in speech_history[-10:]:  # Last 10 speeches
            if 'emotional_state' in speech:
                state = speech['emotional_state']
                recent_states.append({
                    'mood': state.get('core_mood', 'NEUTRAL'),
                    'intensity': state.get('intensity', 0.5),
                    'timestamp': speech.get('timestamp', datetime.now())
                })
        
        if recent_states:
            # Display emotional trend
            moods = [state['mood'] for state in recent_states]
            current_mood = moods[-1]
            mood_changes = len(set(moods))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Mood", current_mood)
            with col2:
                st.metric("Stability", f"{100 - (mood_changes * 10)}%")
            with col3:
                avg_intensity = sum(s['intensity'] for s in recent_states) / len(recent_states)
                st.metric("Avg Intensity", f"{int(avg_intensity * 100)}%")
    
    def render_emotional_insights(self, voice_personality):
        """Render emotional insights and recommendations"""
        emotional_state = voice_personality.emotional_state
        metrics = voice_personality.get_voice_metrics()
        
        st.write("**🧠 Emotional Insights:**")
        
        emotion = emotional_state['core_mood']
        intensity = emotional_state['intensity']
        
        insights = {
            'CONFIDENT': "System is operating with high confidence and reliability.",
            'PROUD': "Recent successes have boosted system morale and performance.",
            'CONTENT': "Stable operation with satisfactory performance levels.",
            'CONCERNED': "Monitoring elevated parameters, increased vigilance recommended.",
            'ANXIOUS': "Critical alerts detected, maximum attention required.",
            'EXCITED': "Excellent performance and positive outcomes detected."
        }
        
        st.info(insights.get(emotion, "System emotional state is neutral."))
        
        # Recommendations based on emotional state
        if emotion in ['CONCERNED', 'ANXIOUS'] and intensity > 0.7:
            st.warning("⚠️ **Recommendation:** Increase monitoring frequency and prepare contingency plans.")
        elif emotion in ['PROUD', 'EXCITED'] and intensity > 0.8:
            st.success("✅ **Recommendation:** Maintain current operational excellence.")
        elif emotion == 'CONFIDENT' and intensity > 0.6:
            st.success("✅ **Recommendation:** Continue with current optimization strategies.")
    
    def create_emotional_avatar(self, emotional_state):
        """Create emotional state avatar visualization"""
        emotion = emotional_state['core_mood']
        intensity = emotional_state['intensity']
        
        avatar_size = int(100 + (intensity * 50))  # Size based on intensity
        
        avatars = {
            'CONFIDENT': '🤖',
            'PROUD': '🌟', 
            'CONTENT': '😊',
            'CONCERNED': '🤔',
            'ANXIOUS': '😰',
            'EXCITED': '🚀'
        }
        
        avatar = avatars.get(emotion, '🤖')
        
        return f"""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: {avatar_size}px;">{avatar}</div>
            <div style="color: #666; margin-top: 10px;">{emotion}</div>
        </div>
        """

# Factory function
def create_emotional_display():
    """Create emotional display instance"""
    return EmotionalDisplay()
