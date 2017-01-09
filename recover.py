import os
import pymongo


def connect_mongodb():
    mongo_ip = "121.40.193.226"
    mongo_port = 27017
    user_name = "root"
    password = "nlpnju"

    mongo_uri = "mongodb://" + user_name + ":" + password + '@' + mongo_ip + ':' + str(mongo_port)
    mongo_connection = pymongo.Connection(mongo_uri)

    return mongo_connection


def check_paper():
    paper_in_file_names = os.listdir("./11-5/")

    mongo_connection = connect_mongodb()
    paper_in_dbs = mongo_connection['GeoPaper']['ChoiceData'].find()

    paper_in_dbs_names = []

    for paper in paper_in_dbs:
        paper_in_dbs_names.append(paper['testpaperName'])

    not_found_in_db_flag = False
    for paper_file_name in paper_in_file_names:
        if paper_file_name.split(".")[0].decode('utf-8') not in paper_in_dbs_names:
            paper_name = paper_file_name.split(".")[0]
            if paper_name:
                print paper_name, "not found in db"
                not_found_in_db_flag = True

    if not not_found_in_db_flag:
        print "all papers in files are found in database"


def recover():
    paper_in_file_names = os.listdir("./11-5/")
    for paper_file_name in paper_in_file_names:
        paper_name = paper_file_name.split(".")[0].decode('utf-8')

        conn = connect_mongodb()
        paper_collections = conn['GeoPaper']['ChoiceData']
        paper_doc = paper_collections.find({'testpaperName': paper_name})

        if not paper_doc:
            print "can't find", paper_name
        else:
            print "found", paper_name


check_paper()
recover()
