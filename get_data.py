import requests
import sqlite3
import json

s = requests.session()

connection = sqlite3.connect("voscreen.db")
cursor = connection.cursor()

# login_url = "https://www.voscreen.com/api/v3/auth/social/facebook/signin/"
#
# login_data = {
#     "access_token": "EAADJo6DMosMBAF0itZBQ0KqnXC2E9Y40qyJb7Kd02vUvTPU4zrEQJJZAO8ZCCbz8pglVS7LlK7tInZCEsDpLPx0NZBCFGaorhrRBCZBGKBOZBS14Si8D57V7Dl2opaijd8Cul7Ndb4mzIAuppJD4E0pIWk7MLw393JqNmbUVH79453wv5mc1oy7VrBQlKZAZBAjQ0sIyz0AJLmgZDZD"
# }
#
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

current_question_id = 4415
video_id = "hclphuflv21k9fna2"

mark = []

while True:
    question_request_data = {"product_name": "voStep", "group_name": "advanced", "current_question_id": 4415,
                             "video_id": "hclphuflv21k9fna2", "language_code": "en"}

    response = s.post(question_url, data=question_request_data)
    ques_res_json = response.content
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

    # print(mark)

    if question_id in mark:
        continue

    mark.append(question_id)

    sql_command = insert_sql.format(
        id=question_id,
        lastitem=int(lastitem),
        liked=int(liked),
        level=level,
        video_subtitle=str(video_subtitle),
        video_distractor=video_distractor,
        video_file=video_file,
        video_metadata_name=video_metadata_name,
        video_metadata_producer=video_metadata_producer,
        video_metadata_director=video_metadata_director,
        video_metadata_details=video_metadata_details,
        video_related_content_url=video_related_content_url,
        video_metadata_views=video_metadata_views,
        video_sources=video_sources,
        language_code=language_code,
        url=url,
        share_url=share_url,
        countdown=countdown,
        choices_answer=choices_answer,
        choices_distractor=choices_distractor
    )

    # print(sql_command)

    cursor.execute(sql_command)
    connection.commit()

    videotype, download_url = video_sources.popitem()

    # print(videotype)
    print(download_url)

    r = requests.get(download_url, allow_redirects=True)
    open('videos/' + video_file + '.' + videotype, 'wb').write(r.content)

    # break
