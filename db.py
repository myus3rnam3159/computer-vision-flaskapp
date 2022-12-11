import pymongo

CONNECTION_STRING = "mongodb+srv://username:mktktd2021@cluster0.x9h69rd.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('objects')
collection = pymongo.collection.Collection(db, 'properties')
