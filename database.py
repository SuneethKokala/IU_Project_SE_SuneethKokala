import os
from supabase import create_client, Client
from datetime import datetime

def get_supabase_client():
    """Get Supabase client"""
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_ANON_KEY')
    return create_client(url, key)

def init_db():
    """Initialize database - Supabase tables created via dashboard"""
    # Tables created via Supabase dashboard SQL editor:
    # incidents, reviews, journeys
    pass

def add_incident(incident_type, location, details, lat=None, lng=None):
    """Add incident to database"""
    supabase = get_supabase_client()
    
    data = {
        'type': incident_type,
        'location': location,
        'details': details,
        'lat': lat,
        'lng': lng
    }
    
    result = supabase.table('incidents').insert(data).execute()
    return result.data[0]['id'] if result.data else None

def add_review(safety_rating, lighting_rating, crowd_rating, comment, lat=None, lng=None):
    """Add review to database"""
    supabase = get_supabase_client()
    
    data = {
        'safety_rating': safety_rating,
        'lighting_rating': lighting_rating,
        'crowd_rating': crowd_rating,
        'comment': comment,
        'lat': lat,
        'lng': lng
    }
    
    result = supabase.table('reviews').insert(data).execute()
    return result.data[0]['id'] if result.data else None

def add_journey(journey_id, user_name, start_lat, start_lng, destination, trusted_contacts):
    """Add journey to database"""
    supabase = get_supabase_client()
    
    data = {
        'journey_id': journey_id,
        'user_name': user_name,
        'start_lat': start_lat,
        'start_lng': start_lng,
        'destination': destination,
        'trusted_contacts': ','.join(trusted_contacts) if trusted_contacts else ''
    }
    
    result = supabase.table('journeys').insert(data).execute()
    return result.data[0]['id'] if result.data else None

def get_incidents():
    """Get all incidents from database"""
    supabase = get_supabase_client()
    
    result = supabase.table('incidents').select('*').order('created_at', desc=True).limit(100).execute()
    
    incidents = []
    for row in result.data:
        incidents.append({
            'type': row['type'],
            'location': row['location'],
            'details': row['details'],
            'lat': row['lat'],
            'lng': row['lng'],
            'timestamp': row['created_at']
        })
    
    return incidents