from pymongo import MongoClient
import os
import traceback
import ssl

# Get MongoDB URI from environment variable
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = "music_recommender_db"

try:
    print(f"Attempting to connect to MongoDB...")
    print(f"Using connection string: {MONGO_URI[:50]}...")  # Print first 50 chars for debugging
    
    # Create SSL context
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    
    # Connect with SSL options
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=30000,
        socketTimeoutMS=30000,
        ssl=True,
        ssl_cert_reqs=ssl.CERT_NONE,
        ssl_match_hostname=False
    )
    
    # Test connection
    client.admin.command('ping')
    print("✅ MongoDB ping successful!")
    
    db = client[DB_NAME]
    songs_collection = db["songs"]
    print("✅ Connected to MongoDB successfully!")
    
    # Test count
    count = songs_collection.count_documents({})
    print(f"✅ Found {count} existing documents")
    
except Exception as e:
    print(f"❌ MongoDB Connection Error: {e}")
    print(f"❌ Error type: {type(e)}")
    print(f"❌ Full traceback: {traceback.format_exc()}")
    songs_collection = None