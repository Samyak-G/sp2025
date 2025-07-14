import re
import numpy as np
from textblob import TextBlob
import json

class EmotionAwareRecommendation:
    def __init__(self):
        # Product categories mapped to emotions
        self.emotion_product_mapping = {
            'happy': ['electronics', 'games', 'books', 'sports'],
            'sad': ['comfort_food', 'books', 'music', 'self_care'],
            'excited': ['electronics', 'games', 'adventure_gear', 'fitness'],
            'stressed': ['wellness', 'books', 'tea', 'aromatherapy'],
            'angry': ['stress_relief', 'books', 'music', 'exercise'],
            'neutral': ['essentials', 'home', 'clothing', 'food']
        }
        
        # Sample products database
        self.products = {
            'electronics': [
                {'id': 1, 'name': 'Smartphone', 'price': 299, 'rating': 4.5},
                {'id': 2, 'name': 'Laptop', 'price': 899, 'rating': 4.3},
                {'id': 3, 'name': 'Headphones', 'price': 79, 'rating': 4.4}
            ],
            'books': [
                {'id': 4, 'name': 'Self-Help Book', 'price': 15, 'rating': 4.2},
                {'id': 5, 'name': 'Fiction Novel', 'price': 12, 'rating': 4.6},
                {'id': 6, 'name': 'Motivational Book', 'price': 18, 'rating': 4.4}
            ],
            'wellness': [
                {'id': 7, 'name': 'Yoga Mat', 'price': 25, 'rating': 4.3},
                {'id': 8, 'name': 'Essential Oils', 'price': 35, 'rating': 4.5},
                {'id': 9, 'name': 'Meditation Cushion', 'price': 45, 'rating': 4.2}
            ]
        }
    
    def analyze_text_sentiment(self, text):
        """Analyze sentiment from text input"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Determine emotion based on polarity
        if polarity > 0.3:
            emotion = 'happy'
        elif polarity < -0.3:
            emotion = 'sad'
        elif polarity > 0.1:
            emotion = 'excited'
        elif polarity < -0.1:
            emotion = 'stressed'
        else:
            emotion = 'neutral'
        
        return {
            'emotion': emotion,
            'polarity': polarity,
            'subjectivity': subjectivity,
            'confidence': abs(polarity)
        }
    
    def analyze_voice_sentiment(self, voice_data):
        """Analyze sentiment from voice input (simulated)"""
        # In real implementation, use speech-to-text and sentiment analysis
        # For now, simulate based on voice characteristics
        import random
        
        emotions = ['happy', 'sad', 'excited', 'stressed', 'neutral']
        detected_emotion = random.choice(emotions)
        
        return {
            'emotion': detected_emotion,
            'confidence': random.uniform(0.6, 0.9),
            'voice_features': {
                'pitch': random.uniform(80, 300),
                'volume': random.uniform(0.3, 0.8),
                'speed': random.uniform(0.8, 1.5)
            }
        }
    
    def get_demographic_preferences(self, user_data):
        """Get preferences based on Indian demographic data"""
        age = user_data.get('age', 25)
        location = user_data.get('location', 'Mumbai')
        income_level = user_data.get('income_level', 'middle')
        
        preferences = {
            'price_sensitivity': 'high' if income_level == 'low' else 'medium',
            'categories': ['electronics', 'home', 'clothing'],
            'brands': ['local', 'international'] if income_level == 'high' else ['local', 'budget']
        }
        
        # Age-based preferences
        if age < 25:
            preferences['categories'].extend(['games', 'fashion'])
        elif age > 45:
            preferences['categories'].extend(['health', 'books'])
        
        return preferences
    
    def recommend_products(self, user_input, user_data):
        """Generate emotion-aware product recommendations"""
        # Analyze emotion from input
        if user_input.get('type') == 'text':
            emotion_data = self.analyze_text_sentiment(user_input['content'])
        else:
            emotion_data = self.analyze_voice_sentiment(user_input.get('voice_data'))
        
        # Get demographic preferences
        demo_preferences = self.get_demographic_preferences(user_data)
        
        # Get emotion-based product categories
        emotion = emotion_data['emotion']
        relevant_categories = self.emotion_product_mapping.get(emotion, ['essentials'])
        
        # Generate recommendations
        recommendations = []
        for category in relevant_categories[:3]:  # Top 3 categories
            if category in self.products:
                category_products = self.products[category]
                # Sort by rating and pick top products
                sorted_products = sorted(category_products, key=lambda x: x['rating'], reverse=True)
                recommendations.extend(sorted_products[:2])  # Top 2 from each category
        
        return {
            'emotion_detected': emotion,
            'confidence': emotion_data['confidence'],
            'recommendations': recommendations,
            'reasoning': f"Based on your {emotion} mood, we recommend these products to enhance your experience"
        }
    
    def personalize_for_indian_market(self, recommendations, user_location):
        """Personalize recommendations for Indian market"""
        # Add cultural context and local preferences
        indian_preferences = {
            'Mumbai': {'trending': ['electronics', 'fashion'], 'local_brands': True},
            'Delhi': {'trending': ['books', 'home'], 'local_brands': True},
            'Bangalore': {'trending': ['electronics', 'books'], 'local_brands': False},
            'Chennai': {'trending': ['books', 'wellness'], 'local_brands': True}
        }
        
        location_prefs = indian_preferences.get(user_location, indian_preferences['Mumbai'])
        
        # Adjust recommendations based on location
        for rec in recommendations:
            if location_prefs['local_brands']:
                rec['local_availability'] = True
                rec['delivery_time'] = '1-2 days'
            else:
                rec['local_availability'] = False
                rec['delivery_time'] = '2-5 days'
        
        return recommendations
