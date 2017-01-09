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

    for paper_file_name in paper_in_file_names:
        if paper_file_name not in paper_in_dbs_names:
            print paper_file_name

check_paper()

