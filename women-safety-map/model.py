import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import requests
import json
from datetime import datetime, timedelta
import math

class AISafetyPredictor:
    def __init__(self):
        self.crime_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.crowd_model = RandomForestRegressor(n_estimators=50, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self._train_models()
    
    def _generate_training_data(self):
        """Generate synthetic training data for crime and crowd prediction"""
        np.random.seed(42)
        n_samples = 1000
        
       
        hours = np.random.randint(0, 24, n_samples)
        days = np.random.randint(0, 7, n_samples)
        weather = np.random.uniform(0, 100, n_samples)  
        police_dist = np.random.uniform(0, 5000, n_samples)  
        population = np.random.uniform(0, 10000, n_samples)  
        
        #
        crime_risk = (
            50 + 
            (24 - hours) * 2 +  
            (100 - weather) * 0.3 +  
            police_dist * 0.01 +  
            np.random.normal(0, 10, n_samples)  
        )
        crime_risk = np.clip(crime_risk, 0, 100)
        
        
        crowd_density = (
            30 +
            np.where(6 <= hours, hours * 3, 0) +  
            np.where(hours <= 18, (18 - hours) * 2, 0) +
            weather * 0.4 +  
            population * 0.003 +
            np.random.normal(0, 15, n_samples)
        )
        crowd_density = np.clip(crowd_density, 0, 100)
        
        features = np.column_stack([hours, days, weather, police_dist, population])
        return features, crime_risk, crowd_density
    
    def _train_models(self):
        """Train ML models with synthetic data"""
        features, crime_risk, crowd_density = self._generate_training_data()
        
        features_scaled = self.scaler.fit_transform(features)
        
        
        self.crime_model.fit(features_scaled, crime_risk)
        self.crowd_model.fit(features_scaled, crowd_density)
        self.is_trained = True
    
    def get_weather_data(self, lat, lng):
        """Get weather data (mock implementation)"""
        try:
            
            weather_conditions = ['clear', 'cloudy', 'rainy', 'stormy']
            condition = np.random.choice(weather_conditions, p=[0.4, 0.3, 0.2, 0.1])
            
            weather_scores = {'clear': 90, 'cloudy': 70, 'rainy': 40, 'stormy': 20}
            return {
                'condition': condition,
                'score': weather_scores[condition],
                'temperature': np.random.uniform(15, 35)
            }
        except:
            return {'condition': 'clear', 'score': 75, 'temperature': 25}
    
    def predict_crime_pattern(self, lat, lng, hour=None, day_of_week=None):
        """Predict crime risk using ML model"""
        if not self.is_trained:
            return 50
        
        if hour is None:
            hour = datetime.now().hour
        if day_of_week is None:
            day_of_week = datetime.now().weekday()
        
        
        weather = self.get_weather_data(lat, lng)
        
        
        police_distance = self._get_nearest_police_distance(lat, lng)
        
        
        population_density = self._estimate_population_density(lat, lng)
        
        
        features = np.array([[hour, day_of_week, weather['score'], 
                            police_distance, population_density]])
        features_scaled = self.scaler.transform(features)
        
        
        crime_risk = self.crime_model.predict(features_scaled)[0]
        return max(0, min(100, crime_risk))
    
    def predict_crowd_density(self, lat, lng, hour=None):
        """Predict crowd density using ML model"""
        if not self.is_trained:
            return 50
        
        if hour is None:
            hour = datetime.now().hour
        
        weather = self.get_weather_data(lat, lng)
        police_distance = self._get_nearest_police_distance(lat, lng)
        population_density = self._estimate_population_density(lat, lng)
        
        features = np.array([[hour, datetime.now().weekday(), weather['score'],
                            police_distance, population_density]])
        features_scaled = self.scaler.transform(features)
        
        crowd_density = self.crowd_model.predict(features_scaled)[0]
        return max(0, min(100, crowd_density))
    
    def forecast_safety_trend(self, lat, lng, hours_ahead=6):
        """Forecast safety trends for next few hours"""
        current_time = datetime.now()
        forecasts = []
        
        for i in range(hours_ahead):
            future_time = current_time + timedelta(hours=i)
            hour = future_time.hour
            day = future_time.weekday()
            
            crime_risk = self.predict_crime_pattern(lat, lng, hour, day)
            crowd_density = self.predict_crowd_density(lat, lng, hour)
            
            
            safety_score = 100 - (crime_risk * 0.7 + (100 - crowd_density) * 0.3)
            
            forecasts.append({
                'time': future_time.strftime('%H:%M'),
                'hour': hour,
                'crime_risk': round(crime_risk, 1),
                'crowd_density': round(crowd_density, 1),
                'safety_score': round(max(0, min(100, safety_score)), 1),
                'recommendation': self._get_safety_recommendation(safety_score)
            })
        
        return forecasts
    
    def _get_nearest_police_distance(self, lat, lng):
        """Calculate distance to nearest police station (mock)"""
        
        police_stations = [
            (18.5204, 73.8567), (18.4899, 73.8056),
            (18.5640, 73.7802), (18.4574, 73.8077)
        ]
        
        min_distance = float('inf')
        for p_lat, p_lng in police_stations:
            distance = self._haversine_distance(lat, lng, p_lat, p_lng)
            min_distance = min(min_distance, distance)
        
        return min_distance
    
    def _estimate_population_density(self, lat, lng):
        """Estimate population density based on location (mock)"""
        
        commercial_zones = [
            (18.5404, 73.8767), (18.5604, 73.7767)  
        ]
        
        base_density = 2000
        for c_lat, c_lng in commercial_zones:
            distance = self._haversine_distance(lat, lng, c_lat, c_lng)
            if distance < 1000:  
                base_density += (1000 - distance) * 5
        
        return min(base_density, 10000)
    
    def _haversine_distance(self, lat1, lng1, lat2, lng2):
        """Calculate distance between two points"""
        R = 6371000  
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_lat/2) * math.sin(delta_lat/2) + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(delta_lng/2) * math.sin(delta_lng/2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
    
    def _get_safety_recommendation(self, safety_score):
        """Get safety recommendation based on score"""
        if safety_score >= 80:
            return "Safe to travel"
        elif safety_score >= 60:
            return "Exercise caution"
        elif safety_score >= 40:
            return "Consider alternative route"
        else:
            return "High risk - avoid if possible"


ai_predictor = AISafetyPredictor()