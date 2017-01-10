#coding=utf-8
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
        if paper_name == "":
            continue

        conn = connect_mongodb()
        paper_collections = conn['GeoPaper']['ChoiceData']
        paper_doc = paper_collections.find({'testpaperName': paper_name})[0]

        file = open("./11-5/" + paper_file_name)

        combined_choice_index = 0
        file.readline()
        for line in file.readlines():
            content_fields = line.split("!@#")

            number = content_fields[get_col_index("number")].split("-")
            timian_number = int(number[0])
            choice_number = '-'.join(number[1:])

            if choice_number == 'A' or choice_number.decode('utf-8') == u'①':
                combined_choice_index = 0
            else:
                combined_choice_index += 1

            question = paper_doc['Questions'][timian_number-1]
            combined_choice = question['combinedTexts'][combined_choice_index]

            # set fields to document
            changed_fields = ['segres', 'segres_fg', 'posres', 'goldtimes', 'goldlocs', 'goldterms', 'goldquants',
                              'topTemplate', 'topTemplateTypes', 'topTemplateCueword',
                              'secondTemplate', 'secondTemplateTypes', 'secondTemplateCueword',
                              'choiceQuestionSentence', 'choice_type', 'qiandao_type', 'core_type', 'core_verb',
                              'delete_part', 'context']

            for field in changed_fields:
                combined_choice[field] = content_fields[get_col_index(field)]

        # set tag states
        must_complete_states = ['seg', 'pos', 'time', 'loc', 'term', 'quant',
                                'newTemplate']
        for state in must_complete_states:
            paper_doc['States'][state] = True

        if 'topTemplate' in paper_doc['States']:
            del paper_doc['States']['topTemplate']
        if 'secondTemplate' in paper_doc['States']:
            del paper_doc['States']['secondTemplate']
        paper_collections.save(paper_doc)

        # may_complete_states = ['background', 'questionInfo']
        checkBackgroundState(paper_name)
        checkGlobalTagQuestionInfoState(paper_name)

        print "finish recovering for:", paper_name

def checkBackgroundState(papername):
    # 连接数据库
    conn = connect_mongodb()
    GeoPaperDB = conn['GeoPaper']

    dataCollection = GeoPaperDB['ChoiceData']
    textFieldName = "combinedTexts"
    paperInfo = dataCollection.find_one({'testpaperName': papername})

    background_state = False
    for question in paperInfo['Questions']:
        for ctext in question[textFieldName]:
            if ctext['delete_part'] != "" or ctext['context'] != "":
                background_state = True

    if background_state:
        print 'background tagged'

    paperInfo['States']['background'] = background_state
    dataCollection.save(paperInfo)
    print "save state to database"


def checkGlobalTagQuestionInfoState(papername):
    # 连接数据库
    conn = connect_mongodb()
    GeoPaperDB = conn['GeoPaper']

    dataCollection = GeoPaperDB['ChoiceData']
    textFieldName = "combinedTexts"
    paperInfo = dataCollection.find_one({'testpaperName': papername})

    question_info_state = True
    for question in paperInfo['Questions']:
        for ctext in question[textFieldName]:
            if ctext['choice_type'] == "":
                question_info_state = False

    if question_info_state:
        print "questionInfo tagged"

    paperInfo['States']['questionInfo'] = question_info_state
    dataCollection.save(paperInfo)


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
