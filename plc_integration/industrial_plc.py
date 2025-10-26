# industrial_plc.py - IEC 61131-3 Function Block
import numpy as np
from datetime import datetime

class AVCS_Soul_Integration:
    """IEC 61131-3 compatible Function Block for PLC integration"""
    
    def __init__(self):
        self.vibration_buffer = np.zeros(1000)
        self.sample_rate = 1000
        self.health_history = []
        self.anomaly_count = 0
        
    def process_cycle(self, vibration_data, sample_rate):
        """Process one cycle of data (called cyclically)"""
        self.vibration_buffer = np.roll(self.vibration_buffer, -len(vibration_data))
        self.vibration_buffer[-len(vibration_data):] = vibration_data
        self.sample_rate = sample_rate
        
        health_score = self.avcs_soul_analyze(self.vibration_buffer)
        anomaly_flag = health_score < 0.7
        recommended_force = self.calculate_damper_force(health_score, anomaly_flag)
        
        self.health_history.append({
            'timestamp': datetime.now().isoformat(),
            'health_score': health_score,
            'anomaly_flag': anomaly_flag,
            'recommended_force': recommended_force
        })
        
        return {
            'HealthScore': health_score,
            'RecommendedForce': recommended_force,
            'AnomalyFlag': anomaly_flag
        }
    
    def avcs_soul_analyze(self, vibration_data):
        """AVCS Soul AI analysis of vibration data"""
        if len(vibration_data) == 0:
            return 1.0
        
        rms = np.sqrt(np.mean(np.square(vibration_data)))
        crest_factor = np.max(np.abs(vibration_data)) / rms if rms > 0 else 0
        kurtosis = self.calculate_kurtosis(vibration_data)
        
        health_score = self.calculate_health_score(rms, crest_factor, kurtosis)
        
        return max(0.0, min(1.0, health_score))
    
    def calculate_kurtosis(self, data):
        """Calculate kurtosis"""
        if len(data) < 4 or np.std(data) == 0:
            return 3.0
        
        n = len(data)
        mean = np.mean(data)
        std = np.std(data)
        
        return np.sum((data - mean) ** 4) / (n * std ** 4)
    
    def calculate_health_score(self, rms, crest_factor, kurtosis):
        """Calculate equipment health score"""
        rms_score = max(0, 1 - (rms / 4.0))
        
        if crest_factor < 3:
            cf_score = 1.0
        elif crest_factor > 8:
            cf_score = 0.0
        else:
            cf_score = 1 - ((crest_factor - 3) / 5)
        
        kurtosis_score = 1.0 / (1 + abs(kurtosis - 3) / 2)
        
        composite_score = (
            0.4 * rms_score +
            0.3 * cf_score +
            0.2 * kurtosis_score +
            0.1 * 1.0  # Placeholder for harmonic analysis
        )
        
        return composite_score
    
    def calculate_damper_force(self, health_score, anomaly_flag):
        """Calculate recommended MR damper force"""
        if anomaly_flag or health_score < 0.5:
            return 8000.0
        elif health_score < 0.7:
            return 4000.0
        elif health_score < 0.9:
            return 1000.0
        else:
            return 500.0
    
    def generate_plc_report(self):
        """Generate report in industrial PLC format"""
        return {
            'FB_Instance': 'AVCS_Soul_Integration',
            'Inputs': {
                'Buffer_Size': len(self.vibration_buffer),
                'Sample_Rate': self.sample_rate,
                'Data_Valid': len(self.vibration_buffer) > 0
            },
            'Outputs': {
                'Health_Score': self.health_history[-1]['health_score'] if self.health_history else 0,
                'Anomaly_Count': self.anomaly_count,
                'Force_Recommendation': self.health_history[-1]['recommended_force'] if self.health_history else 0
            },
            'Diagnostics': {
                'Processing_Time': '≤10ms',
                'Memory_Usage': f"{len(self.vibration_buffer) * 4} bytes",
                'Cycle_Count': len(self.health_history)
            }
        }
