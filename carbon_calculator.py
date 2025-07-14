import requests
import json

class CarbonCalculator:
    def __init__(self):
        # Emission factors (kg CO2 per km)
        self.emission_factors = {
            'truck': 0.12,
            'bike': 0.05,
            'electric_vehicle': 0.02,
            'drone': 0.01
        }
        
        # Fuel consumption rates
        self.fuel_consumption = {
            'truck': 5.5,  # km per liter
            'bike': 45,
            'electric_vehicle': 6,  # km per kWh
            'drone': 20  # km per kWh
        }
    
    def calculate_delivery_emissions(self, delivery_data):
        """Calculate CO2 emissions for delivery"""
        distance = delivery_data.get('distance', 0)
        vehicle_type = delivery_data.get('vehicle_type', 'truck')
        
        # Calculate emissions
        emission_factor = self.emission_factors.get(vehicle_type, 0.12)
        total_emissions = distance * emission_factor
        
        return {
            'distance': distance,
            'vehicle_type': vehicle_type,
            'emissions_kg_co2': round(total_emissions, 2),
            'fuel_consumption': self.calculate_fuel_consumption(distance, vehicle_type)
        }
    
    def calculate_fuel_consumption(self, distance, vehicle_type):
        """Calculate fuel consumption"""
        consumption_rate = self.fuel_consumption.get(vehicle_type, 5.5)
        
        if vehicle_type in ['electric_vehicle', 'drone']:
            return f"{round(distance / consumption_rate, 2)} kWh"
        else:
            return f"{round(distance / consumption_rate, 2)} liters"
    
    def suggest_eco_friendly_options(self, delivery_data):
        """Suggest eco-friendly delivery alternatives"""
        distance = delivery_data.get('distance', 0)
        current_vehicle = delivery_data.get('vehicle_type', 'truck')
        
        suggestions = []
        
        for vehicle, factor in self.emission_factors.items():
            if vehicle != current_vehicle:
                emissions = distance * factor
                savings = (distance * self.emission_factors[current_vehicle]) - emissions
                
                if savings > 0:
                    suggestions.append({
                        'vehicle_type': vehicle,
                        'emissions_kg_co2': round(emissions, 2),
                        'savings_kg_co2': round(savings, 2),
                        'percentage_reduction': round((savings / (distance * self.emission_factors[current_vehicle])) * 100, 1)
                    })
        
        return sorted(suggestions, key=lambda x: x['savings_kg_co2'], reverse=True)
    
    def calculate_carbon_offset_cost(self, emissions_kg):
        """Calculate cost to offset carbon emissions"""
        # Average cost of carbon offset: $15-25 per ton
        cost_per_kg = 0.02  # $0.02 per kg
        return round(emissions_kg * cost_per_kg, 2)
    
    def get_environmental_impact(self, emissions_kg):
        """Convert emissions to relatable environmental impact"""
        # Conversion factors
        trees_needed = emissions_kg / 21  # 1 tree absorbs ~21 kg CO2 per year
        km_by_car = emissions_kg / 0.12  # Average car emissions
        
        return {
            'trees_needed_per_year': round(trees_needed, 1),
            'equivalent_km_by_car': round(km_by_car, 1),
            'phones_charged': round(emissions_kg / 0.008, 0)  # 8g CO2 per phone charge
        }
