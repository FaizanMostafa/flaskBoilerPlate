from pymongo import MongoClient

DB_NAME = ""  
DB_HOST = ""
DB_PORT = ""
DB_USER = "" 
DB_PASS = ""

connection = MongoClient(DB_HOST, DB_PORT, retryWrites=False)
db = connection[DB_NAME]
db.authenticate(DB_USER, DB_PASS)