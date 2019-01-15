import requests
import sqlite3
import json
import os, sys

group_name = input("Difficulty (beginner, elementary, intermediate, upper, advanced): ")

if not os.path.exists('videos/beginner'):
    os.mkdir('videos/beginner')
if not os.path.exists('videos/elementary'):
    os.mkdir('videos/elementary')
if not os.path.exists('videos/intermediate'):
    os.mkdir('videos/intermediate')
if not os.path.exists('videos/upper'):
    os.mkdir('videos/upper')
if not os.path.exists('videos/advanced'):
    os.mkdir('videos/advanced')

if group_name == '':
    group_name = 'advanced'

s = requests.session()

connection = sqlite3.connect("voscreen.db")
cursor = connection.cursor()

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

# login_url = "https://www.voscreen.com/api/v3/auth/social/facebook/signin/"

# login_data = {
#     "access_token": "EAADJo6DMosMBAKdR8mLdamrUJqlaN4xK58k6ZCdHMYPXnrJQDG6MTj1bOY5uizGCVnZCxMQwiXaXHQp67AAAeG2sD4kjx1Ipgwz3JJf402jjBDeuE6rU5Qk1ldBBeRZCiDe4Xk8EuVrUuGHWbIg3iWihvv6VTV4eZA6iSSGSd1IssZAQI6tTm8OnzwLr5kLOWfxY7FO3DagZDZD"
# }

# r = s.post(login_url, data=login_data)
# print(r.content)

question_url = "https://www.voscreen.com/api/v3/game/question/"

insert_sql = 'insert into questions(id, lastitem, liked, level, video_subtitle, video_distractor, video_file,' \
             'video_metadata_name, video_metadata_producer, video_metadata_director, video_metadata_details,' \
             'video_related_content_url, video_metadata_views, video_sources, language_code,' \
             'url, share_url, countdown, choices_answer, choices_distractor) values({id}, {lastitem}, {liked}, {level}, ' \
             '"{video_subtitle}", "{video_distractor}", "{video_file}",' \
             '"{video_metadata_name}", "{video_metadata_producer}", "{video_metadata_director}", "{video_metadata_details}", ' \
             '"{video_related_content_url}", "{video_metadata_views}", "{video_sources}", "{language_code}",' \
             '"{url}", "{share_url}", {countdown}, "{choices_answer}", "{choices_distractor}")'

mark = [-1]
views = []

cnt = 0
current_question_id = 0
while True:

    if cnt == 0:
        question_request_data = {"product_name": "voStep", "group_name": group_name, "language_code": "en",
                                 "viewed": []}
    else:
        question_request_data = {"product_name": "voStep", "group_name": group_name, "language_code": "en",
                                 "current_question_id": current_question_id, "viewed": mark}

    # print(question_request_data)
    cnt = cnt + 1

    response = s.post(question_url, data=question_request_data, headers=headers)
    ques_res_json = response.content
    # print(ques_res_json)
    ques_res_obj = json.loads(ques_res_json)
    question = ques_res_obj["question"]

    lastitem = question["lastitem"]
    liked = question["liked"]
    question_id = question["id"]
    level = question["level"]
    video_subtitle = question["video"]["subtitle"]
    video_distractor = question["video"]["distractor"]
    video_file = question["video"]["file"]
    video_metadata_name = question["video"]["metadata"]["name"]
    video_metadata_producer = question["video"]["metadata"]["producer"]
    video_metadata_director = question["video"]["metadata"]["director"]
    video_metadata_details = question["video"]["metadata"]["details"]
    video_related_content_url = question["video"]["metadata"]["related_content_url"]
    video_metadata_views = question["video"]["metadata"]["views"]
    video_sources = question["video"]["sources"]
    language_code = question["language_code"]
    url = question["url"]
    share_url = question["share_url"]
    countdown = question["countdown"]
    choices_answer = question["choices"]["answer"]
    choices_distractor = question["choices"]["distractor"]

    current_question_id = question_id
    video_id = video_file

    # print(mark)

    # print(question_id)
    # print(mark)

    if question_id in mark:
        print('Duplicated!!!')
        continue

    mark.append(question_id)

    sql_command = insert_sql.format(
        id=question_id,
        lastitem=int(lastitem),
        liked=int(liked),
        level=level,
        video_subtitle=str(video_subtitle).replace('"', ''),
        video_distractor=str(video_distractor).replace('"', ''),
        video_file=str(video_file).replace('"', ''),
        video_metadata_name=str(video_metadata_name).replace('"', ''),
        video_metadata_producer=str(video_metadata_producer).replace('"', ''),
        video_metadata_director=str(video_metadata_director).replace('"', ''),
        video_metadata_details=str(video_metadata_details).replace('"', ''),
        video_related_content_url=str(video_related_content_url).replace('"', ''),
        video_metadata_views=str(video_metadata_views).replace('"', ''),
        video_sources=str(video_sources).replace('"', ''),
        language_code=str(language_code).replace('"', ''),
        url=str(url).replace('"', ''),
        share_url=str(share_url).replace('"', ''),
        countdown=countdown,
        choices_answer=str(choices_answer).replace('"', ''),
        choices_distractor=str(choices_distractor).replace('"', '')
    )

    # print(sql_command)

    try:
        cursor.execute(sql_command)
        connection.commit()
    except Exception as ex:
        print(sql_command)
        print(ex)
        continue

    videotype, download_url = video_sources.popitem()

    # print(videotype)
    print(download_url)

    r = requests.get(download_url, allow_redirects=True)

    open('videos/' + group_name + '/' + video_file + '.' + videotype, 'wb').write(r.content)


    # break
