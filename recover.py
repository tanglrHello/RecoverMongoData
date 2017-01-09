import os
import pymongo

def connect_mongodb():
    mongo_ip = "121.40.193.226"
    mongo_port = 27017
    user_name = "root"
    password = "nlpnju"

    mongo_uri = "mongodb://" + user_name + ":" + password + '@'+ mongo_ip + ':' + str(mongo_port)
    mongo_connection = pymongo.Connection(mongo_uri)

    return mongo_connection

def check_paper():
    paper_in_file_names = os.listdir("./11-5/")
    print paper_in_file_names

    mongo_connection = connect_mongodb()
    print mongo_connection
    paper_in_dbs = mongo_connection['GeoPaper']
    print paper_in_dbs

    paper_in_dbs = paper_in_dbs['ChoiceData']
    print paper_in_dbs

    paper_in_dbs = paper_in_dbs.find()
    print paper_in_dbs

    paper_in_dbs_names = []


    for paper in paper_in_dbs:
        print paper['testpaperName']
    print paper_in_dbs_names

check_paper()

