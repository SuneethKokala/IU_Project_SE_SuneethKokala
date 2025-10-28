from pymongo import MongoClient
from datetime import datetime
import os

class MongoDB:
    def __init__(self):
        mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.client = MongoClient(mongo_uri)
        self.db = self.client['women_safety_db']
    
    def save_emergency_alert(self, data):
        data['timestamp'] = datetime.now()
        return self.db.emergency_alerts.insert_one(data)
    
    def save_incident(self, data):
        data['timestamp'] = datetime.now()
        return self.db.incidents.insert_one(data)
    
    def save_review(self, data):
        data['timestamp'] = datetime.now()
        return self.db.reviews.insert_one(data)
    
    def save_report(self, data):
        data['timestamp'] = datetime.now()
        return self.db.reports.insert_one(data)
    
    def get_reports(self):
        return list(self.db.reports.find({}, {'_id': 0}))

db = MongoDB()