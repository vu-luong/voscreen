import requests
import sqlite3
import json
import os, sys

connection = sqlite3.connect("voscreen.db")
cursor = connection.cursor()

create_command = 'CREATE TABLE if not exists "all_modes" ( id INTEGER PRIMARY KEY, lastitem boolean, liked boolean, level integer, video_subtitle TEXT, video_distractor TEXT, video_file TEXT, video_metadata_name TEXT, video_metadata_producer text, video_metadata_director text, video_metadata_details text, video_related_content_url text, video_metadata_views text, video_sources text, language_code text, url text, share_url text, countdown integer, choices_answer text, choices_distractor text, tags text)'

cursor.execute(create_command)
connection.commit()

modes = ["beginner", "elementary", "intermediate", "upper", "advanced", "am_is_are", "can",
         "will", "what_questions", "imperatives", "was_were", "with_without", "if", "in_at_on",
         "about_for_from", "present_simple", "past_simple", "present_continuous", "present_perfect",
         "relative_clauses", "comparatives_superlatives", "why", "noun_clauses", "adverb_clauses",
         "modals", "passives", "phrasal_verbs", "tenses", "conjunctions", "questions_all", "singular_plural",
         "be_going_to", "1_to_3", "4_to_6", "7_to_9", "10_to_12", "13_and_more", "red", "yellow", "green"]

vo_step = ["beginner", "elementary", "intermediate", "upper", "advanced"]
vo_structure = ["am_is_are", "can",
                "will", "what_questions", "imperatives", "was_were", "with_without", "if", "in_at_on",
                "about_for_from", "present_simple", "past_simple", "present_continuous", "present_perfect",
                "relative_clauses", "comparatives_superlatives", "why", "noun_clauses", "adverb_clauses",
                "modals", "passives", "phrasal_verbs", "tenses", "conjunctions", "questions_all", "singular_plural",
                "be_going_to"]
vo_rhythm = ["1_to_3", "4_to_6", "7_to_9", "10_to_12", "13_and_more"]
vo_kids = ["red", "yellow", "green"]

for mode in modes:
    product = ""
    if mode in vo_step:
        product = 'voStep'
    elif mode in vo_structure:
        product = 'voStructure'
    elif mode in vo_rhythm:
        product = 'voRhythm'
    else:
        product = 'voKids'

    print('Mode = {}'.format(mode))
    select_sql = 'select * from "{mode}"'

    select_command = select_sql.format(mode=mode)

    cursor.execute(select_command)
    lines = cursor.fetchall()

    for line in lines:
        question_id = line[0]
        print(question_id)

        select_from_merger_command = 'select id, tags from "all_modes" where id = {}'.format(question_id)
        cursor.execute(select_from_merger_command)
        datas = cursor.fetchall()
        if len(datas) > 0:
            tags = datas[0][1]
            tags = tags + ', vS::' + product + '::' + mode
            update_sql = 'update "all_modes" set tags="{tags}" where id = {id}'
            update_command = update_sql.format(tags=tags, id=question_id)
            cursor.execute(update_command)
            connection.commit()
        else:
            tags = 'vS::' + product + '::' + mode
            insert_sql = 'insert into "all_modes"(id, lastitem, liked, level, video_subtitle, video_distractor, video_file,' \
                         'video_metadata_name, video_metadata_producer, video_metadata_director, video_metadata_details,' \
                         'video_related_content_url, video_metadata_views, video_sources, language_code,' \
                         'url, share_url, countdown, choices_answer, choices_distractor, tags) values({id}, {lastitem}, {liked}, {level}, ' \
                         '"{video_subtitle}", "{video_distractor}", "{video_file}",' \
                         '"{video_metadata_name}", "{video_metadata_producer}", "{video_metadata_director}", "{video_metadata_details}", ' \
                         '"{video_related_content_url}", "{video_metadata_views}", "{video_sources}", "{language_code}",' \
                         '"{url}", "{share_url}", {countdown}, "{choices_answer}", "{choices_distractor}", "{tags}")'

            insert_command = insert_sql.format(
                id=question_id,
                lastitem=line[1],
                liked=line[2],
                level=line[3],
                video_subtitle=line[4],
                video_distractor=line[5],
                video_file=line[6],
                video_metadata_name=line[7],
                video_metadata_producer=line[8],
                video_metadata_director=line[9],
                video_metadata_details=line[10],
                video_related_content_url=line[11],
                video_metadata_views=line[12],
                video_sources=line[13],
                language_code=line[14],
                url=line[15],
                share_url=line[16],
                countdown=line[17],
                choices_answer=line[18],
                choices_distractor=line[19],
                tags=tags
            )

            cursor.execute(insert_command)
            connection.commit()
