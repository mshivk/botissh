from pymongo import MongoClient

dbname = 'botdbissh'
dbusername = 'botdbuser'
dbpasswd = raw_input("Enter password for mongo db user: ")


connection = MongoClient('ds035026.mlab.com', 35026)
db = connection[dbname]
db.authenticate(dbusername, dbpasswd)
print ' Now in mongoConnect'

def insertOne(dbDoc):
    result = db.conversations.insert_one(dbDoc)
    print " The doc got inserted successfully with Id = {0}",result.inserted_id



