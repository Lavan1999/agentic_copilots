from pymongo import MongoClient
import os
from dotenv import load_dotenv
from bson.binary import Binary
load_dotenv() 


MONGO_URI =os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["copilot_db"]  # fixed DB name

def save_product_idea(title, product_idea, team_metadata, rag_text=None):
    # Clean title to use as collection name:
    collection_name = title.strip().replace(" ", "_").replace("-", "_").lower()
    collection = db[collection_name]
    print("collection_name", collection_name)

    # Check if the document with the same title exists in this collection:
    existing = collection.find_one({"title": title.strip()})
    if existing:
        return "exists"  # Document already present, skip insertion

    document = {
        "title": title.strip(),
        "product_idea": product_idea,
        "rag_text": rag_text,
        "team_metadata": team_metadata
    }

    result = collection.insert_one(document)
    return str(result.inserted_id)

  
def story_file_upload(collection_name):
    collection = db[collection_name]
    # Read Excel file and store as binary
    with open("task_splitup.xlsx", "rb") as file:
        excel_data = file.read()

    collection.insert_one({
        "filename": "task_splitup.xlsx",
        "file": Binary(excel_data),
        "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    })

    print("✅ Excel file uploaded to MongoDB.")