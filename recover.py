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
        paper_doc = paper_collections.find({'testpaperName': paper_name})[0]

        file = open("./11-5/" + paper_file_name)

        combined_choice_index = 0
        file.readline()
        for line in file.readlines():
            fields = line.split("!@#")

            number = fields[get_col_index("number")].split("-")
            timian_number = int(number[0])
            choice_number = '-'.join(number[1:])

            if choice_number == 'A':
                combined_choice_index = 0
            else:
                combined_choice_index += 1

            question = paper_doc['Questions'][timian_number-1]
            combined_choice = question['combinedTexts'][combined_choice_index]

            # set fields to document
            fields = ['segres', 'segres_fg', 'posres', 'goldtimes', 'goldlocs', 'goldterms', 'goldquants',
                      'topTemplate', 'topTemplateTypes', 'topTemplateCueword',
                      'secondTemplate', 'secondTemplateTypes', 'secondTemplateCueword',
                      'choiceQuestionSentence', 'choice_type', 'qiandao_type', 'core_type', 'core_verb',
                      'delete_part', 'context']

            for field in fields:
                try:
                    combined_choice[field] = fields[get_col_index(field)]
                except:
                    print field, len(fields), get_col_index(field)
                    print paper_name
                    print line
                    raise Exception("stop")

        paper_collections.save(paper_doc)


def get_col_index(field_name):
    csv_col_names = ['number',
                     'text',
                     'splitinfo',
                     'segres',
                     'segres_fg',
                     'auto_seg',
                     'auto_seg_fg',
                     'posres',
                     'auto_pos',
                     'goldtimes',
                     'auto_time',
                     'goldlocs',
                     'goldterms',
                     'auto_loc',
                     'goldquants',
                     'bpres',
                     'auto_bpres',
                     'topTemplate',
                     'topTemplateTypes',
                     'topTemplateCueword',
                     'secondTemplate',
                     'secondTemplateTypes',
                     'secondTemplateCueword',
                     'choiceQuestionSentence',
                     'auto_topTemplate',
                     'auto_secondTemplate',
                     'auto_topTemplateCueword',
                     'auto_choiceQuestionSentence',
                     'auto_secondTemplateCueword',
                     'auto_topTemplateTypes',
                     'auto_secondTemplateTypes',
                     'choice_type',
                     'qiandao_type',
                     'core_type',
                     'core_verb',
                     'delete_part',
                     'context']

    return csv_col_names.index(field_name)


check_paper()
recover()
