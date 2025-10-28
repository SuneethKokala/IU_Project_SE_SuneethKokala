"""
Simple localhost startup script for Women Safety Map
"""
import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import pymongo
        import dotenv
        print("All dependencies installed")
        return True
    except ImportError as e:
        print(f" Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def check_mongodb():
    """Check if MongoDB is running"""
    try:
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/')
        client.admin.command('ping')
        print(" MongoDB is running")
        return True
    except Exception as e:
        print(f" MongoDB not running: {e}")
        print("Start MongoDB with: brew services start mongodb-community")
        return False

def main():
    print(" Starting Women Safety Map - Localhost Setup")
    print("=" * 50)
    
    if not check_dependencies():
        sys.exit(1)
    
    if not check_mongodb():
        sys.exit(1)
    
    print("\n Starting Flask application...")
    print(" Main App: http://127.0.0.1:5001")
    print(" Admin Dashboard: http://127.0.0.1:5001/admin")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    os.system("python3 app.py")

if __name__ == "__main__":
    main()