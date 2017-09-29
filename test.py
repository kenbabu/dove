__author__ = 'kenneth'

from flask import Flask,render_template, flash, redirect, url_for, session, request, logging


import pymongo

# Connection to Mongo DB
def db_connection():
    try:
        conn=pymongo.MongoClient()
        print "Connected successfully!!!"
        return conn
    except pymongo.errors.ConnectionFailure, e:
       print "Could not connect to MongoDB: %s" % e
       return False
def get_user(user):
    conn = pymongo.MongoClient()

def main():
    conn=db_connection()
    # print conn.database_names()

    client = pymongo.MongoClient()
    # define a database
    db = client.dove

    results = db.users.find()

    for d in results:
        print d


    #
    # db = conn.diseasese.similarities
    #
    # db.insert_many([{'(disease1, disease2)': 0.94}, {'(disease5, disease3)': 0.64}])
    #
    # results = db.find()
    # #
    # for result in results:
    #     print result
    # # print conn.customerapp.find()

    conn.close()

#      To do
#      Create a collections for similarities


if __name__ == "__main__":
    main()