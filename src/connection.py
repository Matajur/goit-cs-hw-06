"""
Module that provides connection with MongoDB and configures server ports
docker run -d -p 27017:27017 --name <dbname> -e MONGO_INITDB_ROOT_USERNAME=<username> -e MONGO_INITDB_ROOT_PASSWORD=<password> mongo
"""

import os

from motor.motor_asyncio import AsyncIOMotorClient

# config = configparser.ConfigParser()
# config.read("config.ini")

# username = config.get("DB", "user")
# password = config.get("DB", "pass")
# domain = config.get("DB", "domain")
# port = config.get("DB", "port")
# db_name = config.get("DB", "db_name")
# collection = config.get("DB", "collection")

username = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
domain = os.getenv("DB_DOMAIN")
port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
collection = os.getenv("DB_COLLECTION")


async def provide_db_collection():
    """
    Function that provides asynchronous connection to Mongo DB
    """
    client = AsyncIOMotorClient(f"mongodb://{username}:{password}@{domain}:{port}/")
    return client.get_database(db_name).get_collection(collection)


HTTP_SERVER_HOST = os.getenv("HTTP_HOST")
HTTP_SERVER_PORT = int(os.getenv("HTTP_PORT"))

SOCKET_SERVER_HOST = os.getenv("SOCKET_HOST")
SOCKET_SERVER_PORT = os.getenv("SOCKET_PORT")
