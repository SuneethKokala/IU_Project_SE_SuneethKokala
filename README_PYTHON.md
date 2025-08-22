# SafeRoute Pune - Python Flask Version

A Python Flask web application for women's safety navigation in Pune, converted from the original HTML/JavaScript version.

## 🚀 Quick Start

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python run.py
```

### 3. Open in Browser
Navigate to: `http://localhost:5000`

## 🧱 Python Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML, CSS, JavaScript
- **Features**: REST API endpoints for safety analysis

## 📡 API Endpoints

- `GET /` - Main application interface
- `POST /api/analyze-route` - Analyze route safety
- `POST /api/emergency` - Emergency alert system
- `POST /api/report-incident` - Report safety incidents
- `POST /api/submit-review` - Submit route reviews
- `GET /api/safety-zones` - Get Pune safety database

## 🔧 Core Features

✅ **Safety Mode Toggle** - Activate women's safety features
✅ **Route Safety Analysis** - Calculate safety scores based on:
- Police stations proximity
- Hospital locations
- Crime hotspot data
- Time of day factors

✅ **Emergency System** - Location sharing and helpline numbers
✅ **Incident Reporting** - Report unsafe areas or incidents
✅ **Route Reviews** - Community feedback system

## 📊 Safety Algorithm

The Python backend analyzes routes using:
- **Distance calculations** using Haversine formula
- **Safety scoring** based on proximity to safe zones
- **Risk assessment** considering crime hotspots
- **Time-based adjustments** for day/night travel

## 🗺️ Data Points

- 8+ Police stations in Pune
- 5+ Major hospitals
- 4+ Commercial safe zones
- 4+ Known crime hotspots

## 🔄 Differences from Original

**Simplified**:
- No Google Maps integration (coordinates-based)
- Streamlined UI without complex animations
- Core safety logic preserved

**Enhanced**:
- RESTful API architecture
- Server-side safety calculations
- Extensible Python backend

## 🛠️ Development

To extend the application:

1. **Add new safety zones** in `app.py` PUNE_DATABASE
2. **Modify safety algorithm** in `analyze_route_safety()` function
3. **Add new API endpoints** following Flask patterns
4. **Enhance frontend** in `templates/index.html`

## 📱 Usage

1. Click "Activate Women Safety Mode"
2. Enter start/end coordinates (or use auto-detected location)
3. Click "Find Safest Routes Now"
4. View safety analysis with scores and recommendations
5. Use emergency features, incident reporting, and reviews

Perfect for local deployment, testing, and further development of women's safety navigation features.