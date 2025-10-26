import pandas as pd

class DataManager:
    def __init__(self):
        self.max_history = 200
    
    def initialize_dataframes(self):
        return {
            'vibration': pd.DataFrame(),
            'temperature': pd.DataFrame(), 
            'noise': pd.DataFrame(columns=['NOISE']),
            'dampers': pd.DataFrame(),
            'risk_history': []
        }
    
    def add_data_point(self, data_dict, new_data, data_type):
        if data_type not in data_dict:
            data_dict[data_type] = pd.DataFrame()
        
        new_df = pd.DataFrame([new_data])
        if data_dict[data_type].empty:
            updated_df = new_df
        else:
            updated_df = pd.concat([data_dict[data_type], new_df], ignore_index=True)
        
        if len(updated_df) > self.max_history:
            updated_df = updated_df.iloc[-self.max_history:]
        
        data_dict[data_type] = updated_df
        return data_dict
