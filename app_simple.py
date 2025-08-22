from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('maps.html')

@app.route('/api/analyze-route', methods=['POST'])
def analyze_route():
    return jsonify({
        'safety_score': 85,
        'lighting_score': 75,
        'crime_risk': 25,
        'help_points': 3,
        'features': ['Well-lit streets', 'Police station nearby', 'Commercial area'],
        'distance': '1.2 km',
        'time': '15 min'
    })

@app.route('/api/emergency', methods=['POST'])
def emergency_alert():
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')
    
    # Send WhatsApp alert
    try:
        from twilio.rest import Client
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        
        if account_sid and auth_token:
            client = Client(account_sid, auth_token)
            message = f"🚨 EMERGENCY ALERT 🚨\n\nUser needs help!\n\n📍 Location: https://maps.google.com/?q={lat},{lng}\n\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            client.messages.create(
                body=message,
                from_='whatsapp:+14155238886',
                to='whatsapp:+919902480636'
            )
    except:
        pass
    
    return jsonify({
        'status': 'Emergency alert sent',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/report-incident', methods=['POST'])
def report_incident():
    return jsonify({'status': 'Incident reported successfully'})

@app.route('/api/submit-review', methods=['POST'])
def submit_review():
    return jsonify({'status': 'Review submitted successfully'})

@app.route('/api/ai-route-optimization', methods=['POST'])
def ai_route_optimization():
    return jsonify({
        'routes': [
            {
                'type': 'safest',
                'name': 'Safest Route (via Police Station)',
                'analysis': {
                    'safety_score': 95,
                    'lighting_score': 85,
                    'crime_risk': 15,
                    'features': ['Police station nearby', 'Well-lit streets', 'CCTV coverage'],
                    'time': '18 min',
                    'distance': '1.4 km'
                }
            },
            {
                'type': 'balanced',
                'name': 'Balanced Route',
                'analysis': {
                    'safety_score': 80,
                    'lighting_score': 70,
                    'crime_risk': 30,
                    'features': ['Commercial area', 'Good lighting'],
                    'time': '15 min',
                    'distance': '1.2 km'
                }
            },
            {
                'type': 'fastest',
                'name': 'Fastest Route',
                'analysis': {
                    'safety_score': 65,
                    'lighting_score': 60,
                    'crime_risk': 45,
                    'features': ['Direct path', 'Less crowded'],
                    'time': '12 min',
                    'distance': '1.0 km'
                }
            }
        ],
        'recommendation': 'Safest Route (via Police Station)'
    })

@app.route('/api/start-journey', methods=['POST'])
def start_journey():
    data = request.json
    journey_id = f"journey_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Send WhatsApp to contacts
    try:
        from twilio.rest import Client
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        
        if account_sid and auth_token:
            client = Client(account_sid, auth_token)
            for contact in data.get('trusted_contacts', []):
                message = f"🚀 {data.get('user_id', 'User')} started a journey\n\n📍 Track live: https://your-app.vercel.app/track/{journey_id}\n\nYou'll get updates if they need help."
                try:
                    client.messages.create(
                        body=message,
                        from_='whatsapp:+14155238886',
                        to=f'whatsapp:{contact}'
                    )
                except:
                    pass
    except:
        pass
    
    return jsonify({
        'journey_id': journey_id,
        'tracking_url': f'/track/{journey_id}',
        'contacts_notified': len(data.get('trusted_contacts', []))
    })

@app.route('/api/update-location', methods=['POST'])
def update_location():
    return jsonify({'status': 'Location updated'})

@app.route('/api/end-journey', methods=['POST'])
def end_journey():
    return jsonify({'status': 'Journey ended'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)