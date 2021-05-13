import pymongo





client = pymongo.MongoClient("mongodb://rouser:MiLaBiLaFiLa123@127.0.0.1:27017/websecradar?authSource=websecradar")

db = client.websecradar

print(db.list_collection_names())


