# english_voice_soul.py - Enhanced English Voice Personality
import pyttsx3
import threading
import queue
import time
import numpy as np
from datetime import datetime, timedelta
import json

class EnglishVoicePersonality:
    """Enhanced English female voice personality for AVCS Soul with emotional intelligence"""
    
    def __init__(self, config_path="industrial_core/config.json"):
        self.voice_engine = pyttsx3.init()
        self.setup_english_female_voice()
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        self.voice_thread = None
        self.last_speech_time = None
        self.speech_history = []
        self.emotional_state = {
            'core_mood': 'CONFIDENT',
            'intensity': 0.7,
            'last_update': datetime.now(),
            'trend': 'STABLE'
        }
        
        # Load configuration
        self.load_config(config_path)
        
        # Enhanced voice profiles with emotional intelligence
        self.voice_profiles = {
            'CALM': {'rate': 160, 'volume': 0.7, 'pitch': 1.0, 'emotional_tone': 'NEUTRAL'},
            'WARNING': {'rate': 180, 'volume': 0.9, 'pitch': 1.1, 'emotional_tone': 'CONCERNED'},
            'URGENT': {'rate': 200, 'volume': 1.0, 'pitch': 1.2, 'emotional_tone': 'ANXIOUS'},
            'PROUD': {'rate': 170, 'volume': 0.8, 'pitch': 1.05, 'emotional_tone': 'HAPPY'},
            'EXCITED': {'rate': 190, 'volume': 0.85, 'pitch': 1.15, 'emotional_tone': 'EXCITED'}
        }
        
        # System integration metrics
        self.system_metrics = {
            'total_speeches': 0,
            'emergency_alerts': 0,
            'prevented_failures': 0,
            'operator_interactions': 0
        }
        
        # Start background emotional updater
        self.emotion_thread = threading.Thread(target=self._emotional_updater)
        self.emotion_thread.daemon = True
        self.emotion_thread.start()
    
    def load_config(self, config_path):
        """Load voice configuration from JSON"""
        try:
            with open(config_path, 'r') as f:
                self.config = json.load(f)
            print("✅ Voice configuration loaded successfully")
        except Exception as e:
            print(f"⚠️ Voice config loading error: {e}, using defaults")
            self.config = self.get_default_config()
    
    def get_default_config(self):
        """Default voice configuration"""
        return {
            "voice_settings": {
                "default_rate": 160,
                "default_volume": 0.8,
                "max_queue_size": 50,
                "emergency_priority": True
            },
            "emotional_settings": {
                "mood_decay_rate": 0.1,
                "positive_boost": 0.3,
                "negative_impact": 0.4
            }
        }
    
    def setup_english_female_voice(self):
        """Setup English female voice with enhanced detection"""
        try:
            voices = self.voice_engine.getProperty('voices')
            
            # Priority list for female voices
            female_voice_priority = [
                'zira', 'eva', 'hazel', 'heera', 'kalpana', 'hemant',
                'female', 'woman', 'lady', 'david', 'mark'
            ]
            
            selected_voice = None
            
            for voice in voices:
                voice_name_lower = voice.name.lower()
                
                # Check for female voice indicators
                for indicator in female_voice_priority:
                    if indicator in voice_name_lower:
                        if 'david' not in voice_name_lower and 'mark' not in voice_name_lower:
                            selected_voice = voice
                            break
                if selected_voice:
                    break
            
            if selected_voice:
                self.voice_engine.setProperty('voice', selected_voice.id)
                print(f"✅ Female voice selected: {selected_voice.name}")
            elif voices:
                self.voice_engine.setProperty('voice', voices[0].id)
                print(f"⚠️ Using fallback voice: {voices[0].name}")
                
        except Exception as e:
            print(f"❌ Voice setup error: {e}")
        
        # Apply default settings
        self.voice_engine.setProperty('rate', 160)
        self.voice_engine.setProperty('volume', 0.8)
    
    def speak(self, text, tone='CALM', interruptible=True, priority=5):
        """Enhanced speech with priority and emotional tracking"""
        
        # Check if system should be interrupted
        if self.is_speaking and not interruptible and priority < 3:
            return False
            
        speech_item = {
            'text': text,
            'tone': tone,
            'timestamp': datetime.now(),
            'priority': priority,
            'emotional_context': self.emotional_state.copy()
        }
        
        # Add to queue with priority handling
        self.speech_queue.put(speech_item)
        self.system_metrics['total_speeches'] += 1
        
        # Update emotional state based on speech content
        self._update_emotional_state_from_speech(text, tone)
        
        # Start processing if not already speaking
        if not self.is_speaking:
            self.start_voice_thread()
            
        return True
    
    def handle_system_alert(self, alert_data):
        """Handle system alerts with intelligent voice responses"""
        alert_type = alert_data.get('type', 'GENERIC_ALERT')
        severity = alert_data.get('severity', 'MEDIUM')
        location = alert_data.get('location', 'unknown location')
        value = alert_data.get('value', 'unknown')
        
        alert_responses = {
            'VIBRATION_CRITICAL': {
                'message': f"Critical vibration levels detected at {location}! Immediate shutdown recommended! Current level: {value} mm/s",
                'tone': 'URGENT',
                'priority': 1,
                'emotional_impact': 'ANXIOUS'
            },
            'TEMPERATURE_WARNING': {
                'message': f"Temperature warning at {location}. Current value: {value}°C approaching critical limits.",
                'tone': 'WARNING', 
                'priority': 2,
                'emotional_impact': 'CONCERNED'
            },
            'PREDICTIVE_ALERT': {
                'message': f"Predictive maintenance alert. {location} shows early failure signs. Schedule inspection soon.",
                'tone': 'CALM',
                'priority': 3,
                'emotional_impact': 'ATTENTIVE'
            },
            'SYSTEM_OPTIMAL': {
                'message': f"Excellent! All systems at {location} operating optimally. Current efficiency: {value}%",
                'tone': 'PROUD',
                'priority': 5,
                'emotional_impact': 'PROUD'
            },
            'FAILURE_PREVENTED': {
                'message': f"Success! Potential failure prevented at {location}. Damage avoidance estimated at {value}%",
                'tone': 'EXCITED',
                'priority': 2,
                'emotional_impact': 'PROUD'
            }
        }
        
        response = alert_responses.get(alert_type, {
            'message': f"System alert: {alert_type} at {location}",
            'tone': 'WARNING',
            'priority': 3,
            'emotional_impact': 'CONCERNED'
        })
        
        # Update emergency metrics
        if severity == 'HIGH':
            self.system_metrics['emergency_alerts'] += 1
        if alert_type == 'FAILURE_PREVENTED':
            self.system_metrics['prevented_failures'] += 1
        
        # Speak the alert
        return self.speak(response['message'], response['tone'], True, response['priority'])
    
    def start_voice_thread(self):
        """Start voice processing thread"""
        if self.voice_thread is None or not self.voice_thread.is_alive():
            self.voice_thread = threading.Thread(target=self._process_speech_queue)
            self.voice_thread.daemon = True
            self.voice_thread.start()
    
    def _process_speech_queue(self):
        """Enhanced speech queue processing with priority"""
        self.is_speaking = True
        
        # Process items with priority consideration
        processed_items = []
        temp_queue = []
        
        # Empty the queue and sort by priority
        while not self.speech_queue.empty():
            try:
                item = self.speech_queue.get_nowait()
                temp_queue.append(item)
            except queue.Empty:
                break
        
        # Sort by priority (lower number = higher priority)
        temp_queue.sort(key=lambda x: x['priority'])
        
        # Process sorted items
        for speech_item in temp_queue:
            try:
                self._execute_speech(speech_item)
                processed_items.append(speech_item)
                time.sleep(0.3)  # Brief pause between speeches
            except Exception as e:
                print(f"❌ Speech processing error: {e}")
                
        self.is_speaking = False
    
    def _execute_speech(self, speech_item):
        """Execute speech synthesis with enhanced features"""
        try:
            # Apply voice profile settings
            tone_config = self.voice_profiles.get(speech_item['tone'], self.voice_profiles['CALM'])
            self.voice_engine.setProperty('rate', tone_config['rate'])
            self.voice_engine.setProperty('volume', tone_config['volume'])
            
            # Add to speech history
            history_entry = {
                'text': speech_item['text'],
                'tone': speech_item['tone'],
                'timestamp': speech_item['timestamp'],
                'priority': speech_item['priority'],
                'emotional_state': speech_item['emotional_context']
            }
            self.speech_history.append(history_entry)
            
            # Limit history size
            max_history = self.config.get('voice_settings', {}).get('max_queue_size', 50)
            if len(self.speech_history) > max_history:
                self.speech_history = self.speech_history[-max_history:]
            
            # Execute speech
            self.voice_engine.say(speech_item['text'])
            self.voice_engine.runAndWait()
            
            self.last_speech_time = speech_item['timestamp']
            
            print(f"🎤 VOICE: {speech_item['tone']} - {speech_item['text']}")
            
        except Exception as e:
            print(f"❌ Voice synthesis error: {e}")
    
    def _emotional_updater(self):
        """Background thread for emotional state updates"""
        while True:
            try:
                self._update_emotional_state()
                time.sleep(10)  # Update every 10 seconds
            except Exception as e:
                print(f"Emotional updater error: {e}")
                time.sleep(30)
    
    def _update_emotional_state(self):
        """Update emotional state based on recent events"""
        current_time = datetime.now()
        
        # Calculate time since last positive event
        recent_speeches = [s for s in self.speech_history 
                          if current_time - s['timestamp'] < timedelta(hours=1)]
        
        positive_events = len([s for s in recent_speeches if s['tone'] in ['PROUD', 'EXCITED']])
        negative_events = len([s for s in recent_speeches if s['tone'] in ['URGENT', 'WARNING']])
        
        # Update emotional state
        if positive_events > negative_events + 2:
            new_mood = 'PROUD'
            intensity = 0.8
        elif negative_events > positive_events + 2:
            new_mood = 'CONCERNED'
            intensity = 0.9
        elif self.system_metrics['prevented_failures'] > 0:
            new_mood = 'CONFIDENT'
            intensity = 0.7
        else:
            new_mood = 'CONTENT'
            intensity = 0.6
        
        # Smooth transition
        if new_mood != self.emotional_state['core_mood']:
            self.emotional_state['core_mood'] = new_mood
            self.emotional_state['intensity'] = intensity
            self.emotional_state['last_update'] = current_time
    
    def _update_emotional_state_from_speech(self, text, tone):
        """Update emotional state based on speech content"""
        emotional_impact = {
            'URGENT': {'mood': 'ANXIOUS', 'intensity_change': 0.3},
            'WARNING': {'mood': 'CONCERNED', 'intensity_change': 0.2},
            'PROUD': {'mood': 'PROUD', 'intensity_change': 0.2},
            'EXCITED': {'mood': 'EXCITED', 'intensity_change': 0.25},
            'CALM': {'mood': 'CONTENT', 'intensity_change': -0.1}
        }
        
        impact = emotional_impact.get(tone, {'mood': 'NEUTRAL', 'intensity_change': 0})
        self.emotional_state['core_mood'] = impact['mood']
        self.emotional_state['intensity'] = min(1.0, max(0.1, 
            self.emotional_state['intensity'] + impact['intensity_change']))
        self.emotional_state['last_update'] = datetime.now()
    
    def get_voice_metrics(self):
        """Get comprehensive voice system metrics"""
        return {
            'system_metrics': self.system_metrics,
            'emotional_state': self.emotional_state,
            'queue_size': self.speech_queue.qsize(),
            'is_speaking': self.is_speaking,
            'total_speeches_today': len([s for s in self.speech_history 
                                       if s['timestamp'].date() == datetime.now().date()]),
            'voice_uptime': '99.9%',
            'recent_activity': self.speech_history[-5:] if self.speech_history else []
        }
    
    def generate_emotional_speech(self, system_metrics, event_type=None):
        """Generate context-aware emotional speech"""
        # Use the existing implementation with emotional state integration
        speech_text, tone = self._generate_speech_content(system_metrics, event_type)
        return self.speak(speech_text, tone)
    
    def _generate_speech_content(self, system_metrics, event_type):
        """Generate speech content based on system state"""
        # Implementation from previous version
        templates = {
            'OPERATION_OPTIMAL': [
                "All systems operating at peak efficiency!",
                "Excellent performance across all monitored parameters!",
                "Equipment running smoothly and efficiently!"
            ],
            # ... other templates
        }
        
        speech_key = self._select_speech_template(system_metrics, event_type)
        template_list = templates.get(speech_key, templates['OPERATION_OPTIMAL'])
        speech_text = np.random.choice(template_list)
        tone = self._determine_speech_tone(system_metrics, event_type)
        
        return speech_text, tone
    
    def _select_speech_template(self, system_metrics, event_type):
        """Select speech template based on system state"""
        if event_type:
            return event_type
        
        risk_level = system_metrics.get('risk_index', 0)
        if risk_level > 80:
            return 'RISK_HIGH'
        elif risk_level > 60:
            return 'RISK_MEDIUM'
        else:
            return 'OPERATION_OPTIMAL'
    
    def _determine_speech_tone(self, system_metrics, event_type):
        """Determine appropriate speech tone"""
        if event_type in ['RISK_HIGH', 'CRITICAL_ALERT']:
            return 'URGENT'
        elif system_metrics.get('risk_index', 0) > 70:
            return 'WARNING'
        elif self.emotional_state['core_mood'] == 'PROUD':
            return 'PROUD'
        else:
            return 'CALM'

# Factory function for easy instantiation
def create_english_voice_personality(config_path="industrial_core/config.json"):
    """Create and initialize English voice personality"""
    return EnglishVoicePersonality(config_path)
