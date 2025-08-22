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
                'type': 'direct',
                'name': 'Direct Route',
                'analysis': {
                    'safety_score': 85,
                    'lighting_score': 75,
                    'crime_risk': 25,
                    'features': ['Well-lit streets', 'Police station nearby'],
                    'time': '15 min',
                    'distance': '1.2 km'
                }
            }
        ],
        'recommendation': 'Direct Route'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)