# emotional_display.py - Emotional Display Component
import streamlit as st
import plotly.graph_objects as go

class EmotionalDisplay:
    """Component for displaying emotional state"""
    
    def render_emotional_dashboard(self, emotional_state, emotional_display):
        """Render emotional dashboard"""
        
        st.markdown("---")
        st.subheader("🎭 AVCS Soul Emotional State")
        
        # Main emotion display
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            self.render_emotional_gauge(emotional_state)
            
        with col2:
            self.render_emotional_message(emotional_display)
            
        with col3:
            self.render_personality_traits(emotional_state['personality_traits'])
    
    def render_emotional_gauge(self, emotional_state):
        """Render emotional gauge"""
        
        emotion_colors = {
            'ANXIOUS': '#FF6B6B',
            'CONCERNED': '#FFA726', 
            'NEUTRAL': '#42A5F5',
            'CONTENT': '#66BB6A',
            'PROUD': '#AB47BC',
            'CONFIDENT': '#5C6BC0'
        }
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = emotional_state['intensity'] * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"{emotional_state['core_mood']} {emotional_display['emoji']}", 'font': {'size': 20}},
            delta = {'reference': 50, 'increasing': {'color': "RebeccaPurple"}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': emotion_colors.get(emotional_state['core_mood'], "#42A5F5")},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 33], 'color': 'lightgray'},
                    {'range': [33, 66], 'color': 'darkgray'},
                    {'range': [66, 100], 'color': 'gray'}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': emotional_state['intensity'] * 100}
            }
        ))
        
        fig.update_layout(height=300, margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
    
    def render_emotional_message(self, emotional_display):
        """Render emotional message"""
        
        st.markdown(f"""
        <div style="background-color: {emotional_display['mood_color']}20; 
                    padding: 20px; border-radius: 10px; border-left: 5px solid {emotional_display['mood_color']}">
            <h3 style="color: {emotional_display['mood_color']}; margin-top: 0;">
                {emotional_display['emoji']} {emotional_display['message']}
            </h3>
            <p style="color: #666; font-style: italic;">
                {emotional_display['personality_insight']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Additional metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("😰 Stress", f"{emotional_state.get('stress_level', 0)*100:.0f}%")
        with col2:
            st.metric("😊 Satisfaction", f"{emotional_state.get('satisfaction', 0)*100:.0f}%") 
        with col3:
            st.metric("💪 Confidence", f"{emotional_state.get('confidence', 0)*100:.0f}%")
    
    def render_personality_traits(self, personality_traits):
        """Render personality traits"""
        
        st.write("**🧠 Personality Traits:**")
        
        for trait, value in personality_traits.items():
            trait_display = {
                'optimism': 'Optimism',
                'caution': 'Caution', 
                'empathy': 'Empathy',
                'resilience': 'Resilience',
                'curiosity': 'Curiosity'
            }
            
            progress = int(value * 100)
            color = "🟢" if value > 0.7 else "🟡" if value > 0.4 else "🔴"
            
            st.write(f"{color} {trait_display.get(trait, trait)}: {progress}%")
            st.progress(value)
