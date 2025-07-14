import requests
import json
from datetime import datetime
from models import Warehouse, DeliveryRoute, WeatherData
from extensions import db
from sqlalchemy import func

class FulfillmentEngine:
    def __init__(self, db):
        self.db = db

    def get_all_warehouses(self):
        return Warehouse.query.all()
    
    def get_weather_data(self, location):
        # Fetch latest weather data for the location from DB
        return WeatherData.query.filter_by(location=location).order_by(WeatherData.timestamp.desc()).first()
    
    def get_traffic_data(self, route):
        """Get traffic data for route (simulated)"""
        # In real implementation, use Google Maps API or similar
        traffic_levels = ['low', 'moderate', 'high']
        import random
        return {
            'level': random.choice(traffic_levels),
            'estimated_delay': random.randint(0, 60)  # minutes
        }
    
    def select_optimal_warehouse(self, customer_location, order_data):
        # For demo, use the first warehouse as optimal
        warehouses = self.get_all_warehouses()
        if not warehouses:
            return {'warehouse': None, 'estimated_delivery_time': 'N/A'}
        # Example: select the closest warehouse (add real logic as needed)
        best_warehouse = warehouses[0]
        return {
            'warehouse': {
                'id': best_warehouse.id,
                'location': best_warehouse.location
            },
            'estimated_delivery_time': '2h 30m'
        }
    
    def calculate_delivery_time(self, distance, traffic):
        """Calculate estimated delivery time"""
        # Assume average speed of 40 km/h
        base_time = (distance / 40) * 60  # minutes
        
        # Add traffic delay
        total_time = base_time + traffic['estimated_delay']
        
        return f"{int(total_time // 60)}h {int(total_time % 60)}m"
    
    def get_coordinates(self, location):
        """Get coordinates for a location (simplified)"""
        # In real implementation, use geocoding API
        location_coords = {
            'Mumbai': (19.0760, 72.8777),
            'Delhi': (28.6139, 77.2090),
            'Bangalore': (12.9716, 77.5946),
            'Chennai': (13.0827, 80.2707),
            'Pune': (18.5204, 73.8567),
            'Hyderabad': (17.3850, 78.4867)
        }
        return location_coords.get(location, (19.0760, 72.8777))
