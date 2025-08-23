#!/usr/bin/env python3
"""
Database Setup Script for SafeRoute App
This script helps you set up the Supabase database tables.
"""

import os

def print_setup_instructions():
    print("🗄️ SafeRoute Database Setup")
    print("=" * 50)
    
    print("\n📋 Step 1: Create Supabase Account")
    print("1. Go to https://supabase.com")
    print("2. Sign up for a free account")
    print("3. Create a new project")
    
    print("\n🔑 Step 2: Get API Credentials")
    print("1. Go to your project dashboard")
    print("2. Click on Settings > API")
    print("3. Copy the 'URL' and 'anon public' key")
    
    print("\n📝 Step 3: Update Environment Variables")
    print("1. Open the .env file in your project")
    print("2. Replace 'your_supabase_url_here' with your actual URL")
    print("3. Replace 'your_supabase_anon_key_here' with your actual key")
    
    print("\n🏗️ Step 4: Create Database Tables")
    print("1. Go to your Supabase dashboard")
    print("2. Click on 'SQL Editor'")
    print("3. Run the following SQL commands:")
    
    print("\n" + "="*50)
    print("SQL COMMANDS TO RUN:")
    print("="*50)
    
    sql_commands = """
-- Create incidents table
CREATE TABLE incidents (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    location TEXT NOT NULL,
    details TEXT,
    lat DECIMAL(10, 8),
    lng DECIMAL(11, 8),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create reviews table
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    safety_rating INTEGER CHECK (safety_rating >= 1 AND safety_rating <= 5),
    lighting_rating INTEGER CHECK (lighting_rating >= 1 AND lighting_rating <= 5),
    crowd_rating INTEGER CHECK (crowd_rating >= 1 AND crowd_rating <= 5),
    comment TEXT,
    lat DECIMAL(10, 8),
    lng DECIMAL(11, 8),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create journeys table
CREATE TABLE journeys (
    id SERIAL PRIMARY KEY,
    journey_id VARCHAR(100) UNIQUE NOT NULL,
    user_name VARCHAR(100),
    start_lat DECIMAL(10, 8),
    start_lng DECIMAL(11, 8),
    destination TEXT,
    trusted_contacts TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Enable Row Level Security (optional but recommended)
ALTER TABLE incidents ENABLE ROW LEVEL SECURITY;
ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE journeys ENABLE ROW LEVEL SECURITY;

-- Create policies to allow public access (for demo purposes)
CREATE POLICY "Allow public access" ON incidents FOR ALL USING (true);
CREATE POLICY "Allow public access" ON reviews FOR ALL USING (true);
CREATE POLICY "Allow public access" ON journeys FOR ALL USING (true);
"""
    
    print(sql_commands)
    print("="*50)
    
    print("\n✅ Step 5: Test the Connection")
    print("1. Save your changes")
    print("2. Run: python3 test_db.py")
    print("3. You should see successful database operations")
    
    print("\n🚀 Step 6: Deploy to Production")
    print("1. Update your Vercel environment variables")
    print("2. Add SUPABASE_URL and SUPABASE_ANON_KEY")
    print("3. Redeploy your app")
    
    print("\n💡 Troubleshooting:")
    print("- Make sure your Supabase project is active")
    print("- Check that RLS policies allow public access")
    print("- Verify your API keys are correct")
    print("- Check the Supabase logs for errors")

if __name__ == "__main__":
    print_setup_instructions()