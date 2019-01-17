import cv2
import sys
import os
import sqlite3

connection = sqlite3.connect("voscreen.db")
cursor = connection.cursor()

select_command = 'select id, video_file from "all_modes"'
cursor.execute(select_command)
lines = cursor.fetchall()
print(len(lines))
for line in lines:
    filename = line[1]
    print(filename)

    if not os.path.exists('./images'):
        os.makedirs('./images')

    video = cv2.VideoCapture("videos/{}.mp4".format(filename))
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    bins = 4
    marks = []
    for i in range(1, 4):
        marks.append(int(length * i * 1. / bins))

    print(marks)

    # Exit if video not opened.
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()

    cnt = 1
    outcnt = 0
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break

        if cnt in marks:
            outcnt = outcnt + 1
            cv2.imwrite('images/' + filename + '_' + str(outcnt) + '.png', frame)
        cnt = cnt + 1
