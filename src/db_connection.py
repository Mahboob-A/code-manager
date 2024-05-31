
'''
Settings to connect with MondoDB Database running in same Docker Network. 
'''

from pymongo import MongoClient
from django.conf import settings

MONGO_HOST = settings.MONGO_HOST
MONGO_PORT = settings.MONGO_PORT
MONGO_DB_NAME = settings.MONGO_DB_NAME
MONGO_USER = settings.MONGO_USER
MONGO_PASS = settings.MONGO_PASS
MONGO_RESULT_COLLECTIOIN = settings.MONGO_RESULT_COLLECTIOIN
MONGO_AUTH_SOURCE_DB = settings.MONGO_AUTH_SOURCE_DB

# connecting to the mongodb docker contianer.
mongo_client = MongoClient(
    host=MONGO_HOST,
    port=MONGO_PORT,
    username=MONGO_USER,
    password=MONGO_PASS,
    authSource=MONGO_AUTH_SOURCE_DB,
)

# db. 
mongo_result_db = mongo_client[MONGO_DB_NAME]

# collection to save the code execution results. 
mongo_result_collection = mongo_result_db[MONGO_RESULT_COLLECTIOIN]
