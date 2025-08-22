#!/usr/bin/env python3

import requests
import json

BASE_URL = 'http://localhost:8080'

def test_journey_tracking():
    print("🧪 Testing Journey Tracking System")
    print("=" * 40)
    
    # Test 1: Start Journey
    print("\n1. Starting Journey...")
    journey_data = {
        'user_id': 'Test User',
        'start_location': {'lat': 18.5204, 'lng': 73.8567},
        'destination': {'name': 'Phoenix Mall'},
        'trusted_contacts': ['+919902480636']
    }
    
    try:
        response = requests.post(f'{BASE_URL}/api/start-journey', json=journey_data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if response.status_code == 200:
            journey_id = result['journey_id']
            print(f"✅ Journey started with ID: {journey_id}")
            
            # Test 2: Check Journey Status
            print(f"\n2. Checking Journey Status...")
            status_response = requests.get(f'{BASE_URL}/api/journey-status/{journey_id}')
            print(f"Status: {status_response.status_code}")
            status_result = status_response.json()
            print(f"Response: {json.dumps(status_result, indent=2)}")
            
            # Test 3: Update Location
            print(f"\n3. Updating Location...")
            location_data = {
                'journey_id': journey_id,
                'current_location': {'lat': 18.5304, 'lng': 73.8467}
            }
            update_response = requests.post(f'{BASE_URL}/api/update-location', json=location_data)
            print(f"Status: {update_response.status_code}")
            update_result = update_response.json()
            print(f"Response: {json.dumps(update_result, indent=2)}")
            
            # Test 4: Check Status Again
            print(f"\n4. Checking Updated Status...")
            status_response2 = requests.get(f'{BASE_URL}/api/journey-status/{journey_id}')
            status_result2 = status_response2.json()
            print(f"Response: {json.dumps(status_result2, indent=2)}")
            
            print(f"\n🔗 Live Tracking URL: {BASE_URL}/track/{journey_id}")
            
        else:
            print(f"❌ Failed to start journey: {result}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_journey_tracking()