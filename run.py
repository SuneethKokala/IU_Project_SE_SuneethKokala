#!/usr/bin/env python3
"""
SafeRoute   - Women's Safety Navigation System
Run this file to start the Flask web application
"""

from app import app

if __name__ == '__main__':
    print("🛡️ Starting SafeRoute   - Women's Safety Navigation System")
    print("📍 Open your browser and go to: http://localhost:8080")
    print("🚺 Activate Women Safety Mode to start using the features")
    app.run(debug=True, host='0.0.0.0', port=8080)