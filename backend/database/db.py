from pymongo import MongoClient
import os
import ssl
import traceback

# Get MongoDB URI from environment variable
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = "music_recommender_db"

try:
    print(f"Attempting to connect to MongoDB with TLS 1.2...")
    
    # Create a custom SSL context that forces TLS 1.2
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
    ssl_context.maximum_version = ssl.TLSVersion.TLSv1_2
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    # Connect with explicit SSL context
    client = MongoClient(MONGO_URI,
                        serverSelectionTimeoutMS=30000,
                        connectTimeoutMS=30000,
                        socketTimeoutMS=30000,
                        ssl=True,
                        ssl_context=ssl_context)
    
    # Force a connection to test
    client.admin.command('ping')
    print("✅ MongoDB ping successful!")
    
    db = client[DB_NAME]
    songs_collection = db["songs"]
    print("✅ Connected to MongoDB successfully!")
    
    # Test a simple operation
    count = songs_collection.count_documents({})
    print(f"✅ Found {count} existing documents")
    
except Exception as e:
    print(f"❌ MongoDB Connection Error: {e}")
    print(f"❌ Error type: {type(e)}")
    print(f"❌ Full traceback: {traceback.format_exc()}")
    songs_collection = None