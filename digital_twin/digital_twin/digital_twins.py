# digital_twins.py - Industrial Digital Twin
import numpy as np
from scipy import signal
from datetime import datetime

class IndustrialDigitalTwin:
    """Цифровой двойник для виртуального тестирования и прогнозирования"""
    
    def __init__(self, equipment_type="centrifugal_pump"):
        self.equipment_type = equipment_type
        self.health_state = 1.0
        self.operational_hours = 0
        self.failure_modes = self.initialize_failure_modes()
        self.operational_data = self.initialize_operational_data()
        self.simulation_history = []
    
    def initialize_failure_modes(self):
        """Инициализация моделей отказов"""
        return {
            'bearing_wear': {
                'probability': 0.3,
                'progression_rate': 0.001,
                'vibration_impact': 2.5,
                'frequency_characteristic': [2.0, 3.0, 4.0]
            },
            'imbalance': {
                'probability': 0.2, 
                'progression_rate': 0.0005,
                'vibration_impact': 1.8,
                'frequency': 1.0
            },
            'misalignment': {
                'probability': 0.25,
                'progression_rate': 0.0008,
                'vibration_impact': 2.2,
                'frequency_characteristic': [1.0, 2.0]
            },
            'cavitation': {
                'probability': 0.15,
                'progression_rate': 0.002,
                'acoustic_impact': 15.0,
                'random_impacts': True
            }
        }
    
    def initialize_operational_data(self):
        """Инициализация операционных данных"""
        return {
            'baseline_vibration': 1.0,
            'baseline_temperature': 65.0,
            'baseline_noise': 65.0,
            'rpm': 2950,
            'load_profile': 'continuous'
        }
    
    def simulate_equipment_behavior(self, operating_conditions):
        """Симуляция поведения оборудования с учетом состояния"""
        self.operational_hours += 1
        
        self.update_health_state(operating_conditions)
        
        base_vibration = self.generate_base_vibration(operating_conditions)
        
        vibration_data = base_vibration
        if self.health_state < 0.8:
            vibration_data = self.add_bearing_wear(vibration_data)
        if self.health_state < 0.6:
            vibration_data = self.add_imbalance(vibration_data)
        if self.health_state < 0.4:
            vibration_data = self.add_misalignment(vibration_data)
        
        thermal_data = self.simulate_temperature(operating_conditions)
        acoustic_data = self.simulate_acoustics(operating_conditions)
        
        simulation_result = {
            'vibration_data': vibration_data,
            'thermal_data': thermal_data,
            'acoustic_data': acoustic_data,
            'health_metrics': self.calculate_health_metrics(),
            'timestamp': datetime.now().isoformat(),
            'operational_hours': self.operational_hours,
            'predicted_failures': self.predict_failures()
        }
        
        self.simulation_history.append(simulation_result)
        return simulation_result
    
    def generate_base_vibration(self, operating_conditions):
        """Генерация базовой вибрации"""
        rpm = operating_conditions.get('rpm', self.operational_data['rpm'])
        time_vector = np.linspace(0, 1, 1000)
        
        fundamental_freq = rpm / 60.0
        
        vibration_signal = (
            np.sin(2 * np.pi * fundamental_freq * time_vector) +
            0.3 * np.sin(2 * np.pi * 2 * fundamental_freq * time_vector) +
            0.1 * np.sin(2 * np.pi * 3 * fundamental_freq * time_vector) +
            np.random.normal(0, 0.05, len(time_vector))
        )
        
        return {
            'time_domain': vibration_signal,
            'fundamental_frequency': fundamental_freq,
            'rpm': rpm,
            'rms': np.sqrt(np.mean(vibration_signal**2))
        }
    
    def add_bearing_wear(self, base_vibration):
        """Добавление эффектов износа подшипников"""
        time_vector = np.linspace(0, 1, 1000)
        wear_severity = 1.0 - self.health_state
        
        bearing_frequencies = [
            base_vibration['fundamental_frequency'] * 3.1,
            base_vibration['fundamental_frequency'] * 4.8, 
            base_vibration['fundamental_frequency'] * 2.0
        ]
        
        wear_signal = np.zeros_like(time_vector)
        for freq in bearing_frequencies:
            wear_signal += (0.1 * wear_severity * 
                          np.sin(2 * np.pi * freq * time_vector))
        
        base_vibration['time_domain'] += wear_signal
        base_vibration['rms'] = np.sqrt(np.mean(base_vibration['time_domain']**2))
        base_vibration['bearing_wear_indicator'] = wear_severity
        
        return base_vibration
    
    def add_imbalance(self, vibration_data):
        """Добавление эффектов дисбаланса"""
        imbalance_severity = (0.8 - self.health_state) * 2.0
        
        vibration_data['time_domain'] += (
            0.5 * imbalance_severity * 
            np.sin(2 * np.pi * vibration_data['fundamental_frequency'] * 
                  np.linspace(0, 1, len(vibration_data['time_domain'])))
        )
        vibration_data['rms'] = np.sqrt(np.mean(vibration_data['time_domain']**2))
        vibration_data['imbalance_indicator'] = imbalance_severity
        
        return vibration_data
    
    def add_misalignment(self, vibration_data):
        """Добавление эффектов несоосности"""
        misalignment_severity = (0.6 - self.health_state) * 3.0
        
        misalignment_signal = (
            0.3 * misalignment_severity *
            np.sin(2 * np.pi * 2 * vibration_data['fundamental_frequency'] * 
                  np.linspace(0, 1, len(vibration_data['time_domain'])))
        )
        
        vibration_data['time_domain'] += misalignment_signal
        vibration_data['rms'] = np.sqrt(np.mean(vibration_data['time_domain']**2))
        vibration_data['misalignment_indicator'] = misalignment_severity
        
        return vibration_data
    
    def simulate_temperature(self, operating_conditions):
        """Симуляция температурных характеристик"""
        base_temp = self.operational_data['baseline_temperature']
        health_impact = (1.0 - self.health_state) * 20.0
        
        return {
            'motor_winding': base_temp + health_impact + np.random.normal(0, 2),
            'motor_bearing': base_temp + 5 + health_impact + np.random.normal(0, 3),
            'pump_bearing': base_temp + 8 + health_impact + np.random.normal(0, 3),
            'pump_casing': base_temp + 3 + health_impact + np.random.normal(0, 2)
        }
    
    def simulate_acoustics(self, operating_conditions):
        """Симуляция акустических характеристик"""
        base_noise = self.operational_data['baseline_noise']
        health_impact = (1.0 - self.health_state) * 25.0
        
        if self.health_state < 0.5:
            health_impact += 10.0
        
        return base_noise + health_impact + np.random.normal(0, 2)
    
    def update_health_state(self, operating_conditions):
        """Обновление состояния здоровья оборудования"""
        base_degradation = 0.0001
        
        load_penalty = 0.0
        if operating_conditions.get('load', 'normal') == 'high':
            load_penalty = 0.0002
        
        random_failure = np.random.random()
        if random_failure < 0.001:
            self.health_state -= 0.1
        
        self.health_state -= (base_degradation + load_penalty)
        self.health_state = max(0.1, self.health_state)
    
    def calculate_health_metrics(self):
        """Расчет метрик здоровья"""
        return {
            'overall_health': self.health_state,
            'remaining_useful_life': int(self.health_state * 10000),
            'maintenance_urgency': 'HIGH' if self.health_state < 0.3 else 
                                 'MEDIUM' if self.health_state < 0.6 else 'LOW',
            'next_maintenance': int((1.0 - self.health_state) * 30)
        }
    
    def predict_failures(self):
        """Прогнозирование вероятных отказов"""
        predictions = []
        
        for failure_mode, params in self.failure_modes.items():
            probability = params['probability'] * (1.0 - self.health_state)
            
            if probability > 0.1:
                predictions.append({
                    'failure_mode': failure_mode,
                    'probability': probability,
                    'expected_timeframe': f"{int(1/probability)} hours",
                    'severity': 'HIGH' if probability > 0.5 else 
                               'MEDIUM' if probability > 0.3 else 'LOW'
                })
        
        return predictions
    
    def generate_digital_twin_report(self):
        """Генерация отчета цифрового двойника"""
        return {
            'equipment_type': self.equipment_type,
            'current_health': self.health_state,
            'operational_hours': self.operational_hours,
            'simulation_runs': len(self.simulation_history),
            'predicted_failures': self.predict_failures(),
            'maintenance_recommendations': self.generate_maintenance_recommendations(),
            'simulation_timestamp': datetime.now().isoformat()
        }
    
    def generate_maintenance_recommendations(self):
        """Генерация рекомендаций по техническому обслуживанию"""
        recommendations = []
        
        if self.health_state < 0.8:
            recommendations.append("Check bearing lubrication")
        if self.health_state < 0.6:
            recommendations.append("Perform rotor balancing")
        if self.health_state < 0.4:
            recommendations.append("Check shaft alignment")
        if self.health_state < 0.3:
            recommendations.append("SCHEDULE MAJOR OVERHAUL")
        
        return recommendations
