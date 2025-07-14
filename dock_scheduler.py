import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from models import DockSchedule, InventoryItem, Warehouse
from extensions import db

class DockScheduler:
    def __init__(self, db):
        self.db = db
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
        # Find a warehouse (for demo, use the first one)
        warehouse = Warehouse.query.first()
        if not warehouse:
            return {'status': 'no_warehouse_available'}
        # Find next available dock number
        dock_number = 1
        scheduled_time = datetime.now()
        # Create a new dock schedule
        dock_schedule = DockSchedule(
            warehouse_id=warehouse.id,
            truck_id=truck_data.get('truck_id'),
            dock_number=dock_number,
            scheduled_time=scheduled_time,
            estimated_duration=30,
            status='scheduled',
            cargo_type=truck_data.get('cargo_type'),
            truck_size=truck_data.get('size')
        )
        self.db.session.add(dock_schedule)
        self.db.session.commit()
        return {
            'dock_assignment': dock_number,
            'time_slot': scheduled_time.strftime('%H:%M'),
            'status': 'scheduled'
        }
    
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
