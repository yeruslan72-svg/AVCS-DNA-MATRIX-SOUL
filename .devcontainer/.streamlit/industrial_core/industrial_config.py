import json

class IndustrialConfig:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.load_config()
    
    def load_config(self):
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
        except:
            config = self.get_default_config()
        
        # Простой формат как в v5.2
        self.VIBRATION_SENSORS = config['sensors']['vibration']
        self.THERMAL_SENSORS = config['sensors']['thermal']
        self.VIBRATION_LIMITS = config['limits']['vibration']
        self.TEMPERATURE_LIMITS = config['limits']['temperature']
        self.NOISE_LIMITS = config['limits']['noise']
        self.DAMPER_FORCES = config['damper_forces']
    
    def get_default_config(self):
        return {
            "sensors": {
                "vibration": {
                    "VIB_MOTOR_DRIVE": "Motor Drive End",
                    "VIB_MOTOR_NONDRIVE": "Motor Non-Drive End",
                    "VIB_PUMP_INLET": "Pump Inlet Bearing",
                    "VIB_PUMP_OUTLET": "Pump Outlet Bearing"
                },
                "thermal": {
                    "TEMP_MOTOR_WINDING": "Motor Winding",
                    "TEMP_MOTOR_BEARING": "Motor Bearing", 
                    "TEMP_PUMP_BEARING": "Pump Bearing",
                    "TEMP_PUMP_CASING": "Pump Casing"
                }
            },
            "limits": {
                "vibration": {"normal": 2.0, "warning": 4.0, "critical": 6.0},
                "temperature": {"normal": 70, "warning": 85, "critical": 100},
                "noise": {"normal": 70, "warning": 85, "critical": 100}
            },
            "damper_forces": {
                "standby": 500,
                "normal": 1000,
                "warning": 4000, 
                "critical": 8000
            }
        }
