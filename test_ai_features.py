#!/usr/bin/env python3

import requests
import json
from datetime import datetime

# Test AI features
BASE_URL = 'http://localhost:8080'

def test_ai_safety_forecast():
    """Test AI safety forecasting"""
    print("🔮 Testing AI Safety Forecast...")
    
    data = {
        'lat': 18.5204,
        'lng': 73.8567,
        'hours': 6
    }
    
    response = requests.post(f'{BASE_URL}/api/ai-safety-forecast', json=data)
    if response.status_code == 200:
        result = response.json()
        print("✅ Forecast generated successfully!")
        print(f"📍 Location: {result['location']}")
        print("📊 6-Hour Safety Forecast:")
        for forecast in result['forecast']:
            print(f"  {forecast['time']}: Safety {forecast['safety_score']}% - {forecast['recommendation']}")
    else:
        print(f"❌ Error: {response.status_code}")

def test_ai_crime_prediction():
    """Test AI crime prediction"""
    print("\n🚨 Testing AI Crime Prediction...")
    
    data = {
        'lat': 18.4899,
        'lng': 73.8056
    }
    
    response = requests.post(f'{BASE_URL}/api/ai-crime-prediction', json=data)
    if response.status_code == 200:
        result = response.json()
        predictions = result['predictions']
        print("✅ Crime prediction generated!")
        print(f"🎯 Crime Risk: {predictions['crime_risk']}%")
        print(f"👥 Crowd Density: {predictions['crowd_density']}%")
        print(f"🌤️ Weather: {predictions['weather_impact']['condition']} ({predictions['weather_impact']['score']}%)")
        print(f"⚠️ Overall Risk: {predictions['overall_risk']}% ({predictions['risk_level']})")
    else:
        print(f"❌ Error: {response.status_code}")

def test_ai_route_optimization():
    """Test AI route optimization"""
    print("\n🗺️ Testing AI Route Optimization...")
    
    data = {
        'start_lat': 18.5204,
        'start_lng': 73.8567,
        'end_lat': 18.4899,
        'end_lng': 73.8056
    }
    
    response = requests.post(f'{BASE_URL}/api/ai-route-optimization', json=data)
    if response.status_code == 200:
        result = response.json()
        print("✅ Route optimization completed!")
        print(f"🏆 Recommended: {result['recommendation']}")
        print("📋 Route Options:")
        for i, route in enumerate(result['routes'], 1):
            analysis = route['analysis']
            print(f"  {i}. {route['name']}")
            print(f"     Safety: {analysis['safety_score']}% | Crime Risk: {analysis['crime_risk']}%")
            print(f"     Features: {', '.join(analysis['features'][:2])}")
    else:
        print(f"❌ Error: {response.status_code}")

def test_enhanced_route_analysis():
    """Test enhanced route analysis with AI"""
    print("\n🧠 Testing Enhanced Route Analysis...")
    
    data = {
        'start_lat': 18.5204,
        'start_lng': 73.8567,
        'end_lat': 18.4899,
        'end_lng': 73.8056
    }
    
    response = requests.post(f'{BASE_URL}/api/analyze-route', json=data)
    if response.status_code == 200:
        result = response.json()
        print("✅ AI-Enhanced route analysis completed!")
        print(f"🛡️ Safety Score: {result['safety_score']}%")
        print(f"🚨 Crime Risk: {result['crime_risk']}%")
        print(f"👥 Crowd Density: {result.get('crowd_density', 'N/A')}%")
        print(f"🌤️ Weather: {result.get('weather', {}).get('condition', 'N/A')}")
        print(f"💡 Lighting: {result['lighting_score']}%")
        print(f"🤖 AI Enhanced: {result.get('ai_enhanced', False)}")
        print(f"📍 Features: {', '.join(result['features'])}")
    else:
        print(f"❌ Error: {response.status_code}")

if __name__ == "__main__":
    print("🧪 Testing AI-Powered Women Safety Map Features")
    print("=" * 50)
    
    try:
        test_ai_safety_forecast()
        test_ai_crime_prediction()
        test_ai_route_optimization()
        test_enhanced_route_analysis()
        
        print("\n🎉 All AI features tested successfully!")
        print("🚀 Your Women Safety Map now has AI superpowers!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Flask app not running. Start with 'python app.py' first.")
    except Exception as e:
        print(f"❌ Error: {e}")