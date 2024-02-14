import os

# If running on a local machine --> uncomment 2 below line
# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv("../../envs/crawl-dantri.env"))


class Config:
    ROOT_URL = os.environ.get("ROOT-URL")
    DB_NAME = os.environ.get("DB-NAME")
    HOST = os.environ.get("HOST")
    PORT = os.environ.get("PORT")
    HEADER = {
        "Accept": os.environ.get("ACCEPT"),
        "Accept-Encoding": os.environ.get("ACCEPT-ENCODING"),
        "Accept-Language": os.environ.get("ACCEPT-LANGUAGE"),
        "User-Agent": os.environ.get("USER-AGENT"),
    }
    SAVE_TO = os.environ.get("SAVE-TO")
    SAVE_PATH = os.environ.get("SAVE-PATH")
    SAVE_AS = os.environ.get("SAVE-AS")

    PAGINATION = os.environ.get("PAGINATION")
    TIMEOUT = int(os.environ.get("TIMEOUT"))

    USERNAME = os.environ.get("USERNAME")
    PASSWORD = os.environ.get("PASSWORD")
