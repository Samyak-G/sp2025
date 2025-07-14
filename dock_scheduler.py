import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DockScheduler:
    def __init__(self):
        self.dock_capacity = 10
        self.time_slots = self.generate_time_slots()
        self.scheduled_trucks = []
    
    def generate_time_slots(self):
        """Generate available time slots for the day"""
        slots = []
        start_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
        for i in range(20):  # 8 AM to 8 PM, 30-minute slots
            end_time = start_time + timedelta(minutes=30)
            slots.append({
                'start': start_time.strftime('%H:%M'),
                'end': end_time.strftime('%H:%M'),
                'available_docks': self.dock_capacity
            })
            start_time = end_time
        return slots
    
    def predict_unload_time(self, truck_data):
        """Predict unloading time based on truck characteristics"""
        # Simple ML model simulation
        base_time = 30  # Base 30 minutes
        
        # Factors affecting unload time
        size_factor = truck_data.get('size', 'medium')
        cargo_type = truck_data.get('cargo_type', 'general')
        
        if size_factor == 'large':
            base_time += 15
        elif size_factor == 'small':
            base_time -= 10
            
        if cargo_type == 'fragile':
            base_time += 20
            
        return base_time
    
    def schedule_truck(self, truck_data):
        """Schedule truck to optimal dock and time slot"""
        predicted_time = self.predict_unload_time(truck_data)
        
        # Find best available slot
        for i, slot in enumerate(self.time_slots):
            if slot['available_docks'] > 0:
                # Assign truck to this slot
                self.time_slots[i]['available_docks'] -= 1
                
                return {
                    'dock_number': f"Dock {self.dock_capacity - slot['available_docks'] + 1}",
                    'time_slot': f"{slot['start']}-{slot['end']}",
                    'predicted_unload_time': predicted_time,
                    'status': 'scheduled'
                }
        
        return {'status': 'no_slots_available'}
    
    def generate_heatmap_data(self):
        """Generate heatmap data for warehouse optimization"""
        # Simulate product turnover data
        np.random.seed(42)
        zones = ['A', 'B', 'C', 'D', 'E']
        shelves = list(range(1, 21))
        
        heatmap_data = []
        for zone in zones:
            for shelf in shelves:
                turnover_rate = np.random.randint(10, 100)
                heatmap_data.append({
                    'zone': zone,
                    'shelf': shelf,
                    'turnover_rate': turnover_rate,
                    'recommendation': 'high_turnover' if turnover_rate > 70 else 'low_turnover'
                })
        
        return heatmap_data
