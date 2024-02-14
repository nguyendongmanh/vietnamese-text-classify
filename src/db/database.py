import json
from config import Config
from utils.db.db_utils import *
from pymongo import MongoClient

client = MongoClient(
    f"mongodb://{Config.USERNAME}:{Config.PASSWORD}@{Config.HOST}:{Config.PORT}/"
)


def get_database(db_name: str):
    return client[db_name]


def export_collection(
    db_name: str = None,
    path_to_save: str = None,
    file_name: str = None,
    collection_name=None,
):
    db = get_database(db_name)
    posts = list(db[collection_name].find({}, {"_id": 0}))
    with open(f"{path_to_save}/{file_name}.json", "w", encoding="UTF-8") as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)
