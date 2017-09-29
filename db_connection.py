__author__ = 'kenneth'

import pymongo

# Connection to Mongo DB
def db_connection():
    try:
        conn=pymongo.MongoClient()
        print "Connected successfully!!!"
        return conn
    except pymongo.errors.ConnectionFailure, e:
       print "Could not connect to MongoDB: %s" % e

def main():
    db_connection()

if __name__ == "__main__":
    main()
