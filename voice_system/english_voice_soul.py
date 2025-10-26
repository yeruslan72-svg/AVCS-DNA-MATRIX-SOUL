# english_voice_soul.py - English Voice Personality
import pyttsx3
import threading
import queue
import time
import numpy as np
from datetime import datetime

class EnglishVoicePersonality:
    """English female voice personality for AVCS Soul"""
    
    def __init__(self):
        self.voice_engine = pyttsx3.init()
        self.setup_english_female_voice()
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        self.voice_thread = None
        self.last_speech_time = None
        
        self.voice_profiles = {
            'CALM': {'rate': 160, 'volume': 0.7, 'pitch': 1.0},
            'WARNING': {'rate': 180, 'volume': 0.9, 'pitch': 1.1},
            'URGENT': {'rate': 200, 'volume': 1.0, 'pitch': 1.2},
            'PROUD': {'rate': 170, 'volume': 0.8, 'pitch': 1.05},
            'EXCITED': {'rate': 190, 'volume': 0.85, 'pitch': 1.15}
        }
        
    def setup_english_female_voice(self):
        """Setup English female voice"""
        try:
            voices = self.voice_engine.getProperty('voices')
            
            female_voice_ids = []
            for voice in voices:
                voice_name_lower = voice.name.lower()
                if any(female_indicator in voice_name_lower for female_indicator in 
                      ['female', 'zira', 'eva', 'hazel', 'heera', 'kalpana', 'hemant']):
                    female_voice_ids.append(voice.id)
                elif 'david' not in voice_name_lower and 'mark' not in voice_name_lower:
                    female_voice_ids.append(voice.id)
            
            if female_voice_ids:
                self.voice_engine.setProperty('voice', female_voice_ids[0])
                print(f"✅ Female voice selected: {voices[female_voice_ids[0]].name}")
            else:
                if voices:
                    self.voice_engine.setProperty('voice', voices[0].id)
                    print(f"⚠️ Using fallback voice: {voices[0].name}")
                
        except Exception as e:
            print(f"Voice setup warning: {e}")
        
        self.voice_engine.setProperty('rate', 160)
        self.voice_engine.setProperty('volume', 0.8)
        
    def speak(self, text, tone='CALM', interruptible=True):
        """Add speech to queue"""
        if self.is_speaking and not interruptible:
            return False
            
        speech_item = {
            'text': text,
            'tone': tone,
            'timestamp': datetime.now()
        }
        
        self.speech_queue.put(speech_item)
        
        if not self.is_speaking:
            self.start_voice_thread()
            
        return True
    
    def start_voice_thread(self):
        """Start voice processing thread"""
        if self.voice_thread is None or not self.voice_thread.is_alive():
            self.voice_thread = threading.Thread(target=self._process_speech_queue)
            self.voice_thread.daemon = True
            self.voice_thread.start()
    
    def _process_speech_queue(self):
        """Process speech queue"""
        self.is_speaking = True
        
        while not self.speech_queue.empty():
            try:
                speech_item = self.speech_queue.get_nowait()
                self._execute_speech(speech_item)
                time.sleep(0.5)
            except queue.Empty:
                break
                
        self.is_speaking = False
    
    def _execute_speech(self, speech_item):
        """Execute speech synthesis"""
        try:
            tone_config = self.voice_profiles.get(speech_item['tone'], self.voice_profiles['CALM'])
            self.voice_engine.setProperty('rate', tone_config['rate'])
            self.voice_engine.setProperty('volume', tone_config['volume'])
            
            self.voice_engine.say(speech_item['text'])
            self.voice_engine.runAndWait()
            
            self.last_speech_time = speech_item['timestamp']
            
        except Exception as e:
            print(f"Voice synthesis error: {e}")
    
    def generate_emotional_speech(self, emotional_state, system_metrics, event_type=None):
        """Generate emotional speech in English"""
        
        speech_templates = {
            'GREETING': [
                "Hello! AVCS Soul system is ready for operation.",
                "Greetings! I am your equipment monitoring assistant.", 
                "System activated. Ready to ensure your equipment safety."
            ],
            
            'RISK_HIGH': [
                "Attention! Critical vibration levels detected!",
                "Alert! Risk levels have reached dangerous values!",
                "Immediate intervention required! Parameters exceeding safety limits!"
            ],
            
            'RISK_MEDIUM': [
                "Notice: Elevated vibration levels observed. Recommend equipment inspection.",
                "Anomalies detected in operation. Attention advised.",
                "Performance indicators deteriorating. Recommend preventive maintenance."
            ],
            
            'OPERATION_OPTIMAL': [
                "All systems operating optimally! Continuing monitoring.",
                "Parameters within normal range. Equipment running stable and efficient.",
                "Excellent performance! All indicators in the green zone."
            ],
            
            'FAILURE_PREVENTED': [
                "Success! Potential equipment failure prevented!",
                "Excellent work! Major damage has been avoided!", 
                "Critical situation resolved. Equipment is now secure!"
            ],
            
            'MAINTENANCE_REQUIRED': [
                "Equipment requires scheduled maintenance.",
                "Recommend planning service maintenance.",
                "Based on analysis, preventive maintenance will be needed soon."
            ],
            
            'SYSTEM_LEARNING': [
                "New operational patterns detected. Learning and improving!",
                "Analyzing new data. Becoming more effective!",
                "Gained new experience. My predictions are getting more accurate!"
            ],
            
            'EMOTIONAL_HAPPY': [
                "I'm pleased to report excellent system performance today!",
                "Everything is running smoothly! Such a good day for operations!",
                "The equipment is humming along perfectly! I love seeing these numbers!"
            ],
            
            'EMOTIONAL_CONCERNED': [
                "I'm getting concerned about these vibration patterns...",
                "This doesn't look good. We should investigate further.",
                "I have a bad feeling about these readings. Let's be careful."
            ],
            
            'EMOTIONAL_PROUD': [
                "I'm so proud of our team! We just prevented a major incident!",
                "We did it! My algorithms worked perfectly to avoid disaster!",
                "What a great save! Our proactive monitoring just paid off!"
            ]
        }
        
        speech_key = self._select_speech_template(emotional_state, system_metrics, event_type)
        template_list = speech_templates.get(speech_key, speech_templates['OPERATION_OPTIMAL'])
        
        speech_text = np.random.choice(template_list)
        speech_text = self._add_emotional_modifiers(speech_text, emotional_state)
        tone = self._determine_speech_tone(emotional_state, event_type)
        
        return speech_text, tone
    
    def _select_speech_template(self, emotional_state, system_metrics, event_type):
        """Select appropriate speech template"""
        
        if event_type:
            return event_type
            
        risk_level = system_metrics.get('risk_index', 0)
        emotion = emotional_state['core_mood']
        
        if emotion == 'PROUD' and system_metrics.get('prevented_failures', 0) > 0:
            return 'EMOTIONAL_PROUD'
        elif emotion == 'CONTENT' and system_metrics.get('efficiency', 0) > 95:
            return 'EMOTIONAL_HAPPY'
        elif emotion == 'ANXIOUS' and risk_level > 70:
            return 'EMOTIONAL_CONCERNED'
        
        if risk_level > 80:
            return 'RISK_HIGH'
        elif risk_level > 60:
            return 'RISK_MEDIUM'
        elif system_metrics.get('efficiency', 0) > 90:
            return 'OPERATION_OPTIMAL'
        else:
            return 'OPERATION_OPTIMAL'
    
    def _add_emotional_modifiers(self, speech_text, emotional_state):
        """Add emotional modifiers to speech"""
        
        emotion = emotional_state['core_mood']
        intensity = emotional_state['intensity']
        
        emotional_modifiers = {
            'ANXIOUS': ['I must warn you, ', 'Unfortunately, I have to report ', ''],
            'CONCERNED': ['I should mention, ', 'Please note that ', ''],
            'CONTENT': ['I\'m happy to report ', 'It\'s great to see that ', ''],
            'PROUD': ['I\'m proud to announce ', 'It\'s wonderful that ', ''],
            'CONFIDENT': ['I can confidently say ', 'Based on my analysis, ', '']
        }
        
        modifier = np.random.choice(emotional_modifiers.get(emotion, ['', '', '']))
        
        endings = {
            'ANXIOUS': [' Your immediate attention is required!', ' Please take action.', ''],
            'CONCERNED': [' Let\'s keep a close watch.', ' I recommend monitoring this.', ''],
            'CONTENT': [' Keep up the great work!', ' Let\'s maintain this performance!', ''],
            'PROUD': [' Great teamwork!', ' We make an excellent team!', ''],
            'CONFIDENT': [' We have everything under control!', ' The situation is manageable!', '']
        }
        
        ending = np.random.choice(endings.get(emotion, ['', '', '']))
        
        return f"{modifier}{speech_text}{ending}"
    
    def _determine_speech_tone(self, emotional_state, event_type):
        """Determine speech tone"""
        
        if event_type in ['RISK_HIGH', 'CRITICAL_ALERT']:
            return 'URGENT'
        elif emotional_state['core_mood'] in ['ANXIOUS', 'CONCERNED']:
            return 'WARNING'
        elif emotional_state['core_mood'] in ['PROUD', 'CONTENT']:
            return 'EXCITED'
        elif emotional_state['core_mood'] == 'CONFIDENT':
            return 'PROUD'
        else:
            return 'CALM'
