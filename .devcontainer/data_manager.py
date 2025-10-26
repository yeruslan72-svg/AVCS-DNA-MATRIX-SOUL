import json
import pandas as pd

class IndustrialConfig:
    def __init__(self, config_path="industrial_core/config.json"):
        self.config_path = config_path
        self.load_config()
    
    def load_config(self):
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
        except:
            config = self.get_default_config()
        
        # Load configuration with error handling
        try:
            self.APP_VERSION = config['app']['version']
            self.APP_NAME = config['app']['name']
            self.VIBRATION_SENSORS = config['sensors']['vibration']
            self.THERMAL_SENSORS = config['sensors']['thermal']
            self.VIBRATION_LIMITS = config['limits']['vibration']
            self.TEMPERATURE_LIMITS = config['limits']['temperature']
            self.NOISE_LIMITS = config['limits']['noise']
            self.DAMPER_FORCES = config['damper_forces']
            self.DATA_RETENTION = config['system']['data_retention']
            self.REFRESH_RATE = config['system']['refresh_rate']
            self.MAX_CYCLES = config['system']['max_cycles']
        except KeyError as e:
            print(f"Configuration error: {e}. Using defaults for missing values.")
            # Apply defaults for missing values
            default_config = self.get_default_config()
            if 'app' not in config:
                self.APP_VERSION = "6.0"
                self.APP_NAME = "AVCS DNA MATRIX SOUL"
            if 'system' not in config:
                self.DATA_RETENTION = 200
                self.REFRESH_RATE = 0.3
                self.MAX_CYCLES = 500
    
    def get_default_config(self):
        return {
            "app": {
                "version": "6.0",
                "name": "AVCS DNA MATRIX SOUL",
                "description": "Active Vibration Control System DNA MATRIX SOUL"
            },
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
                "vibration": {"normal": 2.0, "warning": 4.0, "critical": 6.0, "emergency": 8.0},
                "temperature": {"normal": 70, "warning": 85, "critical": 100, "emergency": 120},
                "noise": {"normal": 70, "warning": 85, "critical": 100, "emergency": 120}
            },
            "damper_forces": {
                "standby": 500,
                "normal": 1000,
                "warning": 4000, 
                "critical": 8000
            },
            "system": {
                "data_retention": 200,
                "refresh_rate": 0.3,
                "max_cycles": 500
            }
        }

class DataManager:
    def __init__(self, max_history=200):
        self.max_history = max_history
    
    def initialize_dataframes(self):
        """Initialize empty dataframes for all data types"""
        return {
            'vibration': pd.DataFrame(),
            'temperature': pd.DataFrame(), 
            'noise': pd.DataFrame(columns=['NOISE']),
            'dampers': pd.DataFrame(),
            'risk_history': []
        }
    
    def add_data_point(self, data_dict, new_data, data_type):
        """Add new data point to the corresponding dataframe"""
        if data_type not in data_dict:
            data_dict[data_type] = pd.DataFrame()
        
        # Create new dataframe from the data point
        new_df = pd.DataFrame([new_data])
        
        # Concatenate with existing data
        if data_dict[data_type].empty:
            updated_df = new_df
        else:
            updated_df = pd.concat([data_dict[data_type], new_df], ignore_index=True)
        
        # Limit history size
        if len(updated_df) > self.max_history:
            updated_df = updated_df.iloc[-self.max_history:]
        
        data_dict[data_type] = updated_df
        return data_dict
    
    def get_recent_data(self, data_dict, data_type, n_points=10):
        """Get recent n data points from specified data type"""
        if data_type in data_dict and not data_dict[data_type].empty:
            return data_dict[data_type].tail(n_points)
        return pd.DataFrame()
    
    def clear_data(self, data_dict, data_type=None):
        """Clear all data or specific data type"""
        if data_type:
            if data_type in data_dict:
                data_dict[data_type] = pd.DataFrame()
        else:
            for key in data_dict:
                if isinstance(data_dict[key], pd.DataFrame):
                    data_dict[key] = pd.DataFrame()
                else:
                    data_dict[key] = []
        return data_dict
