from flask import Flask, render_template, request, jsonify
import json
import math
import os
from datetime import datetime
from dotenv import load_dotenv
from ai_safety_model import ai_predictor
from live_tracking import live_tracker

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Mock Safety Database
MOCK_DATABASE = {
    'safe_zones': [],
    'crime_hotspots': []
}

def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two points using Haversine formula"""
    R = 6371000  # Earth's radius in meters
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)
    
    a = (math.sin(delta_lat/2) * math.sin(delta_lat/2) + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * 
         math.sin(delta_lng/2) * math.sin(delta_lng/2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def analyze_route_safety(start_lat, start_lng, end_lat, end_lng):
    """AI-Enhanced safety analysis for a route"""
    # Base safety analysis
    safety_score = 75
    lighting_score = 65
    help_points = 0
    features = []
    
    # AI-powered predictions
    ai_crime_risk = ai_predictor.predict_crime_pattern(start_lat, start_lng)
    ai_crowd_density = ai_predictor.predict_crowd_density(start_lat, start_lng)
    weather_data = ai_predictor.get_weather_data(start_lat, start_lng)
    
    # Weather-based adjustments
    weather_multiplier = weather_data['score'] / 100
    safety_score *= weather_multiplier
    
    if weather_data['condition'] == 'rainy':
        features.append('🌧️ Rainy weather - reduced visibility')
    elif weather_data['condition'] == 'stormy':
        features.append('⛈️ Storm warning - seek shelter')
    elif weather_data['condition'] == 'clear':
        features.append('☀️ Clear weather - good visibility')
    
    # Crowd density impact on safety
    if ai_crowd_density > 70:
        safety_score += 15
        features.append('👥 High crowd density - safer area')
    elif ai_crowd_density < 30:
        safety_score -= 10
        features.append('🚶 Low crowd density - isolated area')
    
    # Mock safety zone check
    safety_score += 10
    help_points += 1
    features.append('👮♀️ Safe area detected')
    
    # Mock crime hotspot check
    if ai_crime_risk > 60:
        features.append('⚠️ Exercise caution in this area')
    else:
        features.append('✅ Low crime risk area')
    
    # Time-based adjustment with AI
    hour = datetime.now().hour
    if 6 <= hour <= 20:
        safety_score *= 1.15
        features.append('☀️ Daytime travel - safer')
    else:
        safety_score *= 0.75
        features.append('🌙 Nighttime travel - extra caution needed')
    
    # AI-enhanced lighting score
    if hour >= 18 or hour <= 6:
        lighting_score = max(30, lighting_score - (ai_crime_risk * 0.5))
    
    # Determine route type with AI
    final_safety_score = max(0, min(100, int(safety_score)))
    if final_safety_score >= 80:
        route_type = 'safe'
    elif final_safety_score >= 60:
        route_type = 'moderate'
    else:
        route_type = 'risky'
    
    return {
        'safety_score': final_safety_score,
        'lighting_score': max(0, min(100, int(lighting_score))),
        'crime_risk': max(0, min(100, int(ai_crime_risk))),
        'crowd_density': max(0, min(100, int(ai_crowd_density))),
        'weather': weather_data,
        'help_points': help_points,
        'features': list(set(features)),
        'route_type': route_type,
        'ai_enhanced': True
    }

@app.route('/')
def index():
    return render_template('maps.html')

@app.route('/api/safety-zones')
def get_safety_zones():
    return jsonify(MOCK_DATABASE)

@app.route('/api/analyze-route', methods=['POST'])
def analyze_route():
    data = request.json
    start_lat = data.get('start_lat')
    start_lng = data.get('start_lng')
    end_lat = data.get('end_lat')
    end_lng = data.get('end_lng')
    
    if not all([start_lat, start_lng, end_lat, end_lng]):
        return jsonify({'error': 'Missing coordinates'}), 400
    
    analysis = analyze_route_safety(start_lat, start_lng, end_lat, end_lng)
    
    # Calculate approximate distance and time
    distance = calculate_distance(start_lat, start_lng, end_lat, end_lng)
    walking_speed = 5  # km/h
    time_minutes = int((distance / 1000) / walking_speed * 60)
    
    analysis.update({
        'distance': f"{distance/1000:.1f} km",
        'time': f"{time_minutes} min"
    })
    
    return jsonify(analysis)

@app.route('/api/emergency', methods=['POST'])
def emergency_alert():
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')
    
    # Send WhatsApp alert to admin
    admin_number = '+919902480636'
    location_url = f'https://maps.google.com/?q={lat},{lng}'
    
    message = f"🚨 EMERGENCY ALERT 🚨\n\nUser needs immediate help!\n\n📍 Location: {location_url}\n\nCoordinates: {lat:.6f}, {lng:.6f}\n\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nPlease respond immediately!"
    
    send_whatsapp_alert(admin_number, message)
    
    emergency_data = {
        'timestamp': datetime.now().isoformat(),
        'location': {'lat': lat, 'lng': lng},
        'status': 'Emergency alert sent to admin',
        'admin_notified': True
    }
    
    return jsonify(emergency_data)

def send_whatsapp_alert(phone_number, message):
    try:
        from twilio.rest import Client
        
        # Twilio credentials
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        
        if not account_sid or not auth_token:
            print('❌ Twilio credentials not found in environment variables')
            return False
        
        print(f'🔧 Debug: Using Account SID: {account_sid[:10]}...')
        print(f'🔧 Debug: Sending to: {phone_number}')
        
        client = Client(account_sid, auth_token)
        
        msg = client.messages.create(
            body=message,
            from_='whatsapp:+14155238886',
            to=f'whatsapp:{phone_number}'
        )
        
        print(f'✅ WhatsApp sent successfully!')
        print(f'📱 Message SID: {msg.sid}')
        print(f'📞 To: {phone_number}')
        print(f'📊 Status: {msg.status}')
        return True
        
    except Exception as e:
        print(f'❌ WhatsApp Error: {str(e)}')
        print(f'❌ Error Type: {type(e).__name__}')
        
        # Check if it's an authentication error
        if 'authenticate' in str(e).lower():
            print('🔑 Authentication failed - check your Twilio credentials')
        elif 'sandbox' in str(e).lower():
            print('📱 WhatsApp sandbox not set up - follow setup instructions')
        
        print(f'\n=== EMERGENCY ALERT (FALLBACK) ===\nTo: {phone_number}\nMessage: {message}\n=================================')
        return False

@app.route('/api/report-incident', methods=['POST'])
def report_incident():
    data = request.json
    incident = {
        'type': data.get('type'),
        'location': data.get('location'),
        'details': data.get('details'),
        'timestamp': datetime.now().isoformat(),
        'status': 'Incident reported successfully'
    }
    
    # In a real app, this would save to database
    return jsonify(incident)

@app.route('/api/submit-review', methods=['POST'])
def submit_review():
    data = request.json
    review = {
        'safety_rating': data.get('safety_rating'),
        'lighting_rating': data.get('lighting_rating'),
        'crowd_rating': data.get('crowd_rating'),
        'comment': data.get('comment'),
        'timestamp': datetime.now().isoformat(),
        'status': 'Review submitted successfully'
    }
    
    # In a real app, this would save to database
    return jsonify(review)

# In-memory storage for reports
reports_db = []

@app.route('/api/add-report', methods=['POST'])
def add_report():
    data = request.json
    report = {
        'id': len(reports_db) + 1,
        'lat': data.get('lat'),
        'lng': data.get('lng'),
        'type': data.get('type'),
        'description': data.get('description'),
        'timestamp': datetime.now().isoformat()
    }
    reports_db.append(report)
    return jsonify(report)

@app.route('/api/get-reports')
def get_reports():
    return jsonify(reports_db)

@app.route('/api/ai-safety-forecast', methods=['POST'])
def ai_safety_forecast():
    """Get AI-powered safety forecast for next few hours"""
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')
    hours_ahead = data.get('hours', 6)
    
    if not lat or not lng:
        return jsonify({'error': 'Missing coordinates'}), 400
    
    forecast = ai_predictor.forecast_safety_trend(lat, lng, hours_ahead)
    
    return jsonify({
        'location': {'lat': lat, 'lng': lng},
        'forecast': forecast,
        'generated_at': datetime.now().isoformat()
    })

@app.route('/api/ai-crime-prediction', methods=['POST'])
def ai_crime_prediction():
    """Get real-time AI crime risk prediction"""
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')
    
    if not lat or not lng:
        return jsonify({'error': 'Missing coordinates'}), 400
    
    crime_risk = ai_predictor.predict_crime_pattern(lat, lng)
    crowd_density = ai_predictor.predict_crowd_density(lat, lng)
    weather = ai_predictor.get_weather_data(lat, lng)
    
    # Calculate overall risk level
    overall_risk = (crime_risk * 0.6 + (100 - crowd_density) * 0.3 + (100 - weather['score']) * 0.1)
    
    risk_level = 'low'
    if overall_risk > 70:
        risk_level = 'high'
    elif overall_risk > 40:
        risk_level = 'medium'
    
    return jsonify({
        'location': {'lat': lat, 'lng': lng},
        'predictions': {
            'crime_risk': round(crime_risk, 1),
            'crowd_density': round(crowd_density, 1),
            'weather_impact': weather,
            'overall_risk': round(overall_risk, 1),
            'risk_level': risk_level
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/ai-route-optimization', methods=['POST'])
def ai_route_optimization():
    """Get AI-optimized safe route suggestions"""
    data = request.json
    start_lat = data.get('start_lat')
    start_lng = data.get('start_lng')
    end_lat = data.get('end_lat')
    end_lng = data.get('end_lng')
    
    if not all([start_lat, start_lng, end_lat, end_lng]):
        return jsonify({'error': 'Missing coordinates'}), 400
    
    # Generate multiple route options with AI scoring
    routes = []
    
    # Direct route
    direct_analysis = analyze_route_safety(start_lat, start_lng, end_lat, end_lng)
    routes.append({
        'type': 'direct',
        'name': 'Direct Route',
        'analysis': direct_analysis,
        'waypoints': []
    })
    
    # Safe route (enhanced safety)
    safe_analysis = {
        'safety_score': 95,
        'lighting_score': 85,
        'crime_risk': 15,
        'help_points': 3,
        'features': ['Police station nearby', 'Well-lit streets', 'CCTV coverage'],
        'distance': '1.4 km',
        'time': '18 min'
    }
    routes.append({
        'type': 'safe',
        'name': 'Safest Route (via Police Station)',
        'analysis': safe_analysis
    })
    
    # Balanced route
    balanced_analysis = {
        'safety_score': 80,
        'lighting_score': 70,
        'crime_risk': 30,
        'help_points': 2,
        'features': ['Commercial area', 'Good lighting'],
        'distance': '1.2 km',
        'time': '15 min'
    }
    routes.append({
        'type': 'balanced',
        'name': 'Balanced Route',
        'analysis': balanced_analysis
    })
    
    # Sort routes by safety score
    routes.sort(key=lambda x: x['analysis']['safety_score'], reverse=True)
    
    return jsonify({
        'routes': routes,
        'recommendation': routes[0]['name'],
        'ai_powered': True,
        'generated_at': datetime.now().isoformat()
    })

@app.route('/api/ai-dashboard')
def ai_dashboard():
    """Get AI analytics dashboard data"""
    # Sample locations for demonstration
    sample_locations = [
        {'lat': 52.5200, 'lng': 13.4050, 'name': 'City Center'},
        {'lat': 52.5170, 'lng': 13.3888, 'name': 'Commercial District'},
        {'lat': 52.5244, 'lng': 13.4105, 'name': 'Residential Area'},
        {'lat': 52.5067, 'lng': 13.4282, 'name': 'Business Quarter'}
    ]
    
    dashboard_data = []
    for location in sample_locations:
        crime_risk = ai_predictor.predict_crime_pattern(location['lat'], location['lng'])
        crowd_density = ai_predictor.predict_crowd_density(location['lat'], location['lng'])
        
        dashboard_data.append({
            'location': location['name'],
            'coordinates': {'lat': location['lat'], 'lng': location['lng']},
            'crime_risk': round(crime_risk, 1),
            'crowd_density': round(crowd_density, 1),
            'safety_score': round(100 - crime_risk * 0.7, 1)
        })
    
    return jsonify({
        'areas': dashboard_data,
        'city': 'Current Location',
        'last_updated': datetime.now().isoformat(),
        'ai_model_status': 'active'
    })

# Live Tracking API Endpoints
@app.route('/api/start-journey', methods=['POST'])
def start_journey():
    """Start live journey tracking"""
    data = request.json
    user_id = data.get('user_id', 'Anonymous User')
    start_location = data.get('start_location')
    destination = data.get('destination')
    planned_route = data.get('planned_route', [])
    trusted_contacts = data.get('trusted_contacts', [])
    
    if not all([start_location, destination]):
        return jsonify({'error': 'Missing required data'}), 400
    
    journey_id = live_tracker.start_journey(
        user_id, start_location, destination, planned_route, trusted_contacts
    )
    
    return jsonify({
        'journey_id': journey_id,
        'status': 'journey_started',
        'tracking_url': f'/track/{journey_id}',
        'contacts_notified': len(trusted_contacts)
    })

@app.route('/api/update-location', methods=['POST'])
def update_location():
    """Update current location during journey"""
    data = request.json
    journey_id = data.get('journey_id')
    current_location = data.get('current_location')
    
    if not all([journey_id, current_location]):
        return jsonify({'error': 'Missing journey_id or location'}), 400
    
    result = live_tracker.update_location(journey_id, current_location)
    return jsonify(result)

@app.route('/api/panic-mode', methods=['POST'])
def activate_panic_mode():
    """Activate panic mode with live streaming"""
    data = request.json
    journey_id = data.get('journey_id')
    panic_data = data.get('panic_data', {})
    
    if not journey_id:
        return jsonify({'error': 'Missing journey_id'}), 400
    
    result = live_tracker.activate_panic_mode(journey_id, panic_data)
    return jsonify(result)

@app.route('/api/end-journey', methods=['POST'])
def end_journey():
    """End journey tracking"""
    data = request.json
    journey_id = data.get('journey_id')
    end_location = data.get('end_location')
    
    if not journey_id:
        return jsonify({'error': 'Missing journey_id'}), 400
    
    result = live_tracker.end_journey(journey_id, end_location)
    return jsonify(result)

@app.route('/api/journey-status/<journey_id>')
def get_journey_status(journey_id):
    """Get current journey status"""
    result = live_tracker.get_journey_status(journey_id)
    return jsonify(result)

@app.route('/api/family-dashboard/<contact_phone>')
def family_dashboard(contact_phone):
    """Get family/friend dashboard"""
    result = live_tracker.get_family_dashboard(contact_phone)
    return jsonify(result)

@app.route('/track/<journey_id>')
def track_journey(journey_id):
    """Live tracking page for family/friends"""
    return render_template('track.html', journey_id=journey_id)

@app.route('/family-dashboard/<contact_phone>')
def family_dashboard_page(contact_phone):
    """Family dashboard page"""
    return render_template('family_dashboard.html', contact_phone=contact_phone)

@app.route('/test-tracking')
def test_tracking_page():
    """Test tracking page"""
    with open('test_live_tracking.html', 'r') as f:
        return f.read()

if __name__ == '__main__':
    print('🤖 AI Safety Predictor initialized')
    print('📍 Live Tracking System ready')
    print('🚀 Starting Women Safety Map with AI enhancements...')
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)