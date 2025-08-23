import os
import psycopg2
from datetime import datetime

def get_db_connection():
    """Get database connection using Vercel Postgres"""
    return psycopg2.connect(os.environ.get('POSTGRES_URL'))

def init_db():
    """Initialize database tables"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create incidents table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id SERIAL PRIMARY KEY,
            type VARCHAR(50) NOT NULL,
            location VARCHAR(255) NOT NULL,
            details TEXT,
            lat DECIMAL(10, 8),
            lng DECIMAL(11, 8),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create reviews table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id SERIAL PRIMARY KEY,
            safety_rating INTEGER NOT NULL,
            lighting_rating INTEGER NOT NULL,
            crowd_rating INTEGER NOT NULL,
            comment TEXT,
            lat DECIMAL(10, 8),
            lng DECIMAL(11, 8),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create journeys table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS journeys (
            id SERIAL PRIMARY KEY,
            journey_id VARCHAR(100) UNIQUE NOT NULL,
            user_name VARCHAR(100) NOT NULL,
            start_lat DECIMAL(10, 8),
            start_lng DECIMAL(11, 8),
            destination VARCHAR(255),
            trusted_contacts TEXT,
            status VARCHAR(20) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    cur.close()
    conn.close()

def add_incident(incident_type, location, details, lat=None, lng=None):
    """Add incident to database"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        INSERT INTO incidents (type, location, details, lat, lng)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    ''', (incident_type, location, details, lat, lng))
    
    incident_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return incident_id

def add_review(safety_rating, lighting_rating, crowd_rating, comment, lat=None, lng=None):
    """Add review to database"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        INSERT INTO reviews (safety_rating, lighting_rating, crowd_rating, comment, lat, lng)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    ''', (safety_rating, lighting_rating, crowd_rating, comment, lat, lng))
    
    review_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return review_id

def add_journey(journey_id, user_name, start_lat, start_lng, destination, trusted_contacts):
    """Add journey to database"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    contacts_str = ','.join(trusted_contacts) if trusted_contacts else ''
    
    cur.execute('''
        INSERT INTO journeys (journey_id, user_name, start_lat, start_lng, destination, trusted_contacts)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    ''', (journey_id, user_name, start_lat, start_lng, destination, contacts_str))
    
    db_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return db_id

def get_incidents():
    """Get all incidents from database"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        SELECT type, location, details, lat, lng, created_at
        FROM incidents
        ORDER BY created_at DESC
        LIMIT 100
    ''')
    
    incidents = []
    for row in cur.fetchall():
        incidents.append({
            'type': row[0],
            'location': row[1],
            'details': row[2],
            'lat': float(row[3]) if row[3] else None,
            'lng': float(row[4]) if row[4] else None,
            'timestamp': row[5].isoformat() if row[5] else None
        })
    
    cur.close()
    conn.close()
    return incidents