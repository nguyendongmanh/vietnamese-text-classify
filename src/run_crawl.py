from config import Config
from pymongo import UpdateOne
from crawl.dantri import crawl as dantri
from db.database import get_database, export_collection


def main():
    crawl_db = get_database(Config.DB_NAME)
    # print(Config.HEADER)
    print(f"FROM {Config.ROOT_URL}")
    topics = dantri.get_topics(Config.ROOT_URL)
    if Config.SAVE_TO == "db":
        topic_count = crawl_db["dantri_topics"].count_documents({})
        update_topics = [
            UpdateOne({"name": topic["name"]}, {"$set": topic}, upsert=True)
            for topic in topics
        ]
        if topic_count == 0:
            print("Collection is empty, insert ...")
        # update topics
        else:
            print("Update all records in `dantri_topics` collection")
        crawl_db["dantri_topics"].bulk_write(update_topics)

        for topic in topics:
            total_posts = 0
            for topic_link in topic["link"]:
                posts = dantri.walk_topic(topic["name"], topic_link)
                if len(posts) > 0:
                    update_posts = [
                        UpdateOne(
                            {"title": post["title"]}, {"$set": post}, upsert=True
                        )
                        for post in posts
                    ]
                # Insert to `dantri` collection
                crawl_db["dantri"].bulk_write(update_posts)
                total_posts += len(posts)
            print(f"There are {total_posts} posts being scraped in {topic['name']}")

        print("Export to data/ ... ")
        export_collection(
            "mydb",
            path_to_save="data",
            file_name="dantri",
            collection_name="dantri",
        )

    else:
        pass


if __name__ == "__main__":
    main()
