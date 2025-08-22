import json
import uuid
from datetime import datetime, timedelta
from threading import Timer
import math

class LiveTrackingManager:
    def __init__(self):
        self.active_journeys = {}
        self.trusted_contacts = {}
        self.location_history = {}
        self.route_deviations = {}
    
    def start_journey(self, user_id, start_location, destination, planned_route, trusted_contacts):
        """Start live journey tracking"""
        journey_id = str(uuid.uuid4())
        
        journey_data = {
            'journey_id': journey_id,
            'user_id': user_id,
            'start_time': datetime.now().isoformat(),
            'start_location': start_location,
            'destination': destination,
            'planned_route': planned_route,
            'trusted_contacts': trusted_contacts,
            'current_location': start_location,
            'status': 'active',
            'last_update': datetime.now().isoformat(),
            'deviation_alerts': [],
            'panic_mode': False
        }
        
        self.active_journeys[journey_id] = journey_data
        self.location_history[journey_id] = [start_location]
        
        # Send start notification to trusted contacts
        self._notify_journey_start(journey_data)
        
        # Set up auto-check timer (5 minutes)
        self._schedule_check_in(journey_id)
        
        return journey_id
    
    def update_location(self, journey_id, current_location):
        """Update current location during journey"""
        if journey_id not in self.active_journeys:
            return {'error': 'Journey not found'}
        
        journey = self.active_journeys[journey_id]
        journey['current_location'] = current_location
        journey['last_update'] = datetime.now().isoformat()
        
        # Add to location history
        self.location_history[journey_id].append({
            'location': current_location,
            'timestamp': datetime.now().isoformat()
        })
        
        # Check for route deviation
        deviation = self._check_route_deviation(journey_id, current_location)
        if deviation:
            self._handle_route_deviation(journey_id, deviation)
        
        # Notify trusted contacts of location update
        self._notify_location_update(journey)
        
        return {'status': 'updated', 'deviation': deviation}
    
    def activate_panic_mode(self, journey_id, panic_data=None):
        """Activate panic mode with live streaming"""
        if journey_id not in self.active_journeys:
            return {'error': 'Journey not found'}
        
        journey = self.active_journeys[journey_id]
        journey['panic_mode'] = True
        journey['panic_activated'] = datetime.now().isoformat()
        
        if panic_data:
            journey['panic_data'] = panic_data
        
        # Send immediate panic alerts
        self._send_panic_alerts(journey)
        
        # Start live streaming simulation
        self._start_live_streaming(journey_id)
        
        return {'status': 'panic_activated', 'emergency_contacts_notified': True}
    
    def end_journey(self, journey_id, end_location=None):
        """End journey tracking"""
        if journey_id not in self.active_journeys:
            return {'error': 'Journey not found'}
        
        journey = self.active_journeys[journey_id]
        journey['status'] = 'completed'
        journey['end_time'] = datetime.now().isoformat()
        
        if end_location:
            journey['end_location'] = end_location
        
        # Notify trusted contacts of safe arrival
        self._notify_journey_end(journey)
        
        # Archive journey
        del self.active_journeys[journey_id]
        
        return {'status': 'journey_ended', 'contacts_notified': True}
    
    def get_journey_status(self, journey_id):
        """Get current journey status"""
        if journey_id not in self.active_journeys:
            return {'error': 'Journey not found'}
        
        journey = self.active_journeys[journey_id]
        location_history = self.location_history.get(journey_id, [])
        
        return {
            'journey': journey,
            'location_history': location_history[-10:],  # Last 10 locations
            'total_locations': len(location_history)
        }
    
    def get_family_dashboard(self, contact_phone):
        """Get dashboard for family/friends"""
        active_journeys_for_contact = []
        
        for journey_id, journey in self.active_journeys.items():
            if contact_phone in journey.get('trusted_contacts', []):
                journey_info = {
                    'journey_id': journey_id,
                    'user_id': journey['user_id'],
                    'start_time': journey['start_time'],
                    'current_location': journey['current_location'],
                    'destination': journey['destination'],
                    'status': journey['status'],
                    'last_update': journey['last_update'],
                    'panic_mode': journey.get('panic_mode', False),
                    'deviation_alerts': journey.get('deviation_alerts', [])
                }
                active_journeys_for_contact.append(journey_info)
        
        return {
            'active_journeys': active_journeys_for_contact,
            'contact_phone': contact_phone,
            'last_updated': datetime.now().isoformat()
        }
    
    def _check_route_deviation(self, journey_id, current_location):
        """Check if user has deviated from planned route"""
        journey = self.active_journeys[journey_id]
        planned_route = journey.get('planned_route', [])
        
        if not planned_route:
            return None
        
        # Calculate distance from planned route
        min_distance = float('inf')
        for route_point in planned_route:
            distance = self._calculate_distance(
                current_location['lat'], current_location['lng'],
                route_point['lat'], route_point['lng']
            )
            min_distance = min(min_distance, distance)
        
        # If more than 200m from route, consider it a deviation
        if min_distance > 200:
            return {
                'distance_from_route': min_distance,
                'current_location': current_location,
                'timestamp': datetime.now().isoformat()
            }
        
        return None
    
    def _handle_route_deviation(self, journey_id, deviation):
        """Handle route deviation alert"""
        journey = self.active_journeys[journey_id]
        
        # Add to deviation alerts
        if 'deviation_alerts' not in journey:
            journey['deviation_alerts'] = []
        
        journey['deviation_alerts'].append(deviation)
        
        # Send alert to trusted contacts
        self._send_deviation_alert(journey, deviation)
    
    def _notify_journey_start(self, journey_data):
        """Notify trusted contacts that journey has started"""
        message = f"🚀 Journey Started\n\n{journey_data['user_id']} has started their journey to {journey_data['destination']['name']}\n\n📍 Live tracking: http://localhost:8080/track/{journey_data['journey_id']}\n\nYou'll receive updates during the journey."
        
        for contact in journey_data['trusted_contacts']:
            self._send_notification(contact, message)
    
    def _notify_location_update(self, journey_data):
        """Send periodic location updates to trusted contacts"""
        # Only send updates every 5 minutes to avoid spam
        last_update = datetime.fromisoformat(journey_data['last_update'])
        if (datetime.now() - last_update).seconds < 300:  # 5 minutes
            return
        
        location = journey_data['current_location']
        message = f"📍 Location Update\n\n{journey_data['user_id']} is currently at:\nLat: {location['lat']:.6f}\nLng: {location['lng']:.6f}\n\n🗺️ View: https://maps.google.com/?q={location['lat']},{location['lng']}"
        
        for contact in journey_data['trusted_contacts']:
            self._send_notification(contact, message)
    
    def _notify_journey_end(self, journey_data):
        """Notify trusted contacts of safe arrival"""
        message = f"✅ Safe Arrival\n\n{journey_data['user_id']} has safely reached their destination!\n\nJourney completed at {datetime.now().strftime('%H:%M')}"
        
        for contact in journey_data['trusted_contacts']:
            self._send_notification(contact, message)
    
    def _send_panic_alerts(self, journey_data):
        """Send immediate panic alerts to all contacts"""
        location = journey_data['current_location']
        message = f"🚨 PANIC ALERT 🚨\n\n{journey_data['user_id']} has activated panic mode!\n\n📍 Current Location:\nhttps://maps.google.com/?q={location['lat']},{location['lng']}\n\n🔴 IMMEDIATE ASSISTANCE NEEDED\n\nCall 100 (Police) or 108 (Emergency)"
        
        # Send to trusted contacts
        for contact in journey_data['trusted_contacts']:
            self._send_notification(contact, message)
        
        # Also send to emergency services (admin)
        admin_message = f"🚨 PANIC MODE ACTIVATED 🚨\n\nUser: {journey_data['user_id']}\nLocation: {location['lat']:.6f}, {location['lng']:.6f}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nIMMEDIATE RESPONSE REQUIRED!"
        self._send_notification('+919902480636', admin_message)
    
    def _send_deviation_alert(self, journey_data, deviation):
        """Send route deviation alert"""
        message = f"⚠️ Route Deviation Alert\n\n{journey_data['user_id']} has deviated from their planned route by {deviation['distance_from_route']:.0f}m\n\n📍 Current location:\nhttps://maps.google.com/?q={deviation['current_location']['lat']},{deviation['current_location']['lng']}\n\nTime: {datetime.now().strftime('%H:%M')}"
        
        for contact in journey_data['trusted_contacts']:
            self._send_notification(contact, message)
    
    def _start_live_streaming(self, journey_id):
        """Start live streaming simulation"""
        journey = self.active_journeys[journey_id]
        journey['live_streaming'] = {
            'active': True,
            'stream_url': f'http://localhost:8080/live-stream/{journey_id}',
            'started_at': datetime.now().isoformat()
        }
    
    def _send_notification(self, phone_number, message):
        """Send notification via WhatsApp"""
        from app import send_whatsapp_alert
        send_whatsapp_alert(phone_number, message)
    
    def _calculate_distance(self, lat1, lng1, lat2, lng2):
        """Calculate distance between two points"""
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
    
    def _schedule_check_in(self, journey_id):
        """Schedule automatic check-in"""
        def check_in():
            if journey_id in self.active_journeys:
                journey = self.active_journeys[journey_id]
                last_update = datetime.fromisoformat(journey['last_update'])
                
                # If no update for 10 minutes, send alert
                if (datetime.now() - last_update).seconds > 600:
                    self._send_check_in_alert(journey)
        
        # Schedule check in 10 minutes
        timer = Timer(600.0, check_in)
        timer.start()
    
    def _send_check_in_alert(self, journey_data):
        """Send check-in alert if no recent updates"""
        message = f"⏰ Check-in Alert\n\nNo location update from {journey_data['user_id']} for 10+ minutes.\n\nLast known location:\nhttps://maps.google.com/?q={journey_data['current_location']['lat']},{journey_data['current_location']['lng']}\n\nPlease check on them."
        
        for contact in journey_data['trusted_contacts']:
            self._send_notification(contact, message)

# Global tracking manager
live_tracker = LiveTrackingManager()