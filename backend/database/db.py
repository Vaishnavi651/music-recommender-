from pymongo import MongoClient
import os
import certifi
import traceback

# Get MongoDB URI from environment variable
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = "music_recommender_db"

try:
    print(f"Attempting to connect to MongoDB...")
    # Use tlsCAFile=certifi.where() to handle SSL certificates
    client = MongoClient(MONGO_URI, 
                        serverSelectionTimeoutMS=10000,
                        tlsCAFile=certifi.where())
    # Force a connection to test
    client.admin.command('ping')
    print("✅ MongoDB ping successful!")
    
    db = client[DB_NAME]
    songs_collection = db["songs"]
    print("✅ Connected to MongoDB successfully!")
    
except Exception as e:
    print(f"❌ MongoDB Connection Error: {e}")
    print(f"❌ Error type: {type(e)}")
    print(f"❌ Full traceback: {traceback.format_exc()}")
    songs_collection = None