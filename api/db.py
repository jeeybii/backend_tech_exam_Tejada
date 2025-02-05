from motor.motor_asyncio import AsyncIOMotorClient
import os

# MongoDB Connection String
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = "medalists_db"

# Initialize MongoDB Client
client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]

# Collections
medalists_collection = db["medalists"]

# Function to set up necessary indexes
async def setup_indexes():
    """ Create indexes for faster querying """
    await medalists_collection.create_index([("code_athlete", 1), ("event", 1)], unique=True)
    await medalists_collection.create_index([("medal_date", -1)])  
    await medalists_collection.create_index([("discipline", 1)])  

# Bulk Insert Medalists
async def insert_medalists_bulk(medalists_data: list):
    """ Insert multiple medalists into the database efficiently. """
    if not medalists_data:
        return []

    result = await medalists_collection.insert_many(medalists_data)
    return result.inserted_ids

# Insert Single Medalist
async def insert_medalist(medalist_data: dict):
    """ Insert a single medalist into the database. """
    result = await medalists_collection.insert_one(medalist_data)
    return result.inserted_id

# Check for Existing Medalist (Prevents Duplicates)
async def find_existing_medalist(code_athlete: int, event: str, medal_date: str, medal_type: str):
    """ Check if a medalist already exists using unique identifiers. """
    return await medalists_collection.find_one(
        {
            "code_athlete": code_athlete,
            "event": event,
            "medal_date": medal_date,
            "medal_type": medal_type
        }
    )
