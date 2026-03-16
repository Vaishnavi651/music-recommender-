from pymongo import MongoClient
import os
import traceback

# Get MongoDB URI from environment variable
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = "music_recommender_db"

try:
    print(f"Attempting to connect to MongoDB...")
    
    # SIMPLE connection - no extra parameters!
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=30000)
    
    # Test connection
    client.admin.command('ping')
    print("✅ MongoDB ping successful!")
    
    db = client[DB_NAME]
    songs_collection = db["songs"]
    print("✅ Connected to MongoDB successfully!")
    
except Exception as e:
    print(f"❌ MongoDB Connection Error: {e}")
    songs_collection = None