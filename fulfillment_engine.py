import requests
import json
from datetime import datetime

class FulfillmentEngine:
    def __init__(self):
        self.warehouses = [
            {'id': 'WH001', 'location': 'Mumbai', 'coordinates': (19.0760, 72.8777)},
            {'id': 'WH002', 'location': 'Delhi', 'coordinates': (28.6139, 77.2090)},
            {'id': 'WH003', 'location': 'Bangalore', 'coordinates': (12.9716, 77.5946)},
            {'id': 'WH004', 'location': 'Chennai', 'coordinates': (13.0827, 80.2707)}
        ]
        
    def calculate_distance(self, coord1, coord2):
        """Calculate distance between two coordinates"""
        # Simplified distance calculation
        import math
        
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of earth in kilometers
        r = 6371
        return c * r
    
    def get_weather_data(self, location):
        """Get weather data for location (simulated)"""
        # In real implementation, use actual weather API
        weather_conditions = ['clear', 'rain', 'heavy_rain', 'fog']
        import random
        return {
            'condition': random.choice(weather_conditions),
            'temperature': random.randint(15, 35),
            'humidity': random.randint(40, 90)
        }
    
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
        """Select best warehouse based on multiple factors"""
        customer_coords = self.get_coordinates(customer_location)
        
        warehouse_scores = []
        
        for warehouse in self.warehouses:
            # Calculate distance
            distance = self.calculate_distance(warehouse['coordinates'], customer_coords)
            
            # Get weather and traffic data
            weather = self.get_weather_data(warehouse['location'])
            traffic = self.get_traffic_data(f"{warehouse['location']}-{customer_location}")
            
            # Calculate score (lower is better)
            score = distance * 0.4  # Distance weight
            
            # Weather penalty
            if weather['condition'] == 'heavy_rain':
                score += 50
            elif weather['condition'] == 'rain':
                score += 20
            
            # Traffic penalty
            if traffic['level'] == 'high':
                score += 30
            elif traffic['level'] == 'moderate':
                score += 15
            
            warehouse_scores.append({
                'warehouse': warehouse,
                'score': score,
                'distance': distance,
                'weather': weather,
                'traffic': traffic,
                'estimated_delivery_time': self.calculate_delivery_time(distance, traffic)
            })
        
        # Select warehouse with lowest score
        best_warehouse = min(warehouse_scores, key=lambda x: x['score'])
        return best_warehouse
    
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
