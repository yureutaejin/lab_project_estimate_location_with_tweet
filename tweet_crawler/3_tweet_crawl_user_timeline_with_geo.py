# -*- coding: utf-8 -*-
import json
import sys
import tweepy
import time

# Consumer keys and access tokens, used for OAuth
consumer_key="T4OmeH7ZrH2jB8tPBMwuitlzv"
consumer_secret="NnlVSq6eGLAZM0HcptsmsEXJ22wrbCkhkOYLZ32EcSniyHXRv7"
access_token="1455834250054287362-pVWjp2r5TAJdcNT2K9GPtLsSujeAD3"
access_token_secret="Lg1WOe8CJT7qb5UmTz5PVPY1Yfm5J041lokEVBFAQ5BBU"

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

# creat file name based on user id


# get username from json file
"""
with open('./UserData/DetroitInDetroitusers.json',encoding="UTF-8") as js_file:
    js_file = js_file.read()
    js_data = json.loads(js_file)
    countlen = len(js_data["notyet"])

users = [0]*countlen

for i in range(countlen):
        users[i] = js_data["notyet"][i]["screen_name"]

users = list(dict.fromkeys(users))
"""

# 한 방에 돌릴 때 사용
# location_name = ['Boston', 'San Francisco']
# second_result_data_name_list = ['Detroit', 'Jacksonville', 'San Francisco', 'Washington, DC']

second_result_data_name_list = ['Fort Worth']

for city_name in second_result_data_name_list:
    # 실제로 해당도시가 location으로 등록되어있는 username 추출 (리스트로 형식으로 자동 중복 제거)
    with open('/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/tweet_data/2_result_data/{}_remove_repeat_user.json'.format(city_name), 'r', encoding="UTF-8") as tw_file:
        tw_file = tw_file.read()
        tw_data = json.loads(tw_file)
        usernum = len(tw_data['users'])

    userlist = []

    for i in range(usernum):
        if (city_name in tw_data['users'][i]["location"]):
            tw_name = tw_data['users'][i]['screen_name']
            userlist.append(tw_name)

    userlist = list(dict.fromkeys(userlist))

    users = userlist

    print("시작")
    with open('/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/tweet_data/3_result_data/{}_user_timeline_with_coord7.json'.format(city_name), 'w', encoding='utf-8') as newsfile:
        #print("시작")
        sys.stdout = newsfile
        print("{\"users\":[")
        for i in range(len(users)):
            user_name = str("@" + users[i])
            print("{\"id\":\"" + user_name + "\"," + "\"timeline\":[")
            try:
                for status in tweepy.Cursor(api.user_timeline, screen_name=user_name, tweet_mode="extended").items():
                    # print(status)
                    Coords = dict()
                    XY = []

                    if status.geo is not None:
                        Coords.update(status.geo.coordinates)
                        XY = (Coords.get('coordinates'))
                    else:
                        XY = (0.0, 0.0)

                    if status.coordinates is not None:
                        Coords.update(status.coordinates)
                        XY = (Coords.get('coordinates'))
                    else:
                        XY = (0.0, 0.0)

                    if status.place is not None:
                        if status.place.full_name is not None:
                            place = status.place.full_name
                        else:
                            place = "null"
                    else:
                        place = "null"

                    date = str(status.created_at)
                    date = date.split(" ")[0]
                    if '2022' in date:
                        continue
                    if '2021' in date:
                        continue
                    if '2020' in date:
                        continue
                    if '2019' in date:
                        continue
                    if '2018' in date:
                        text = str(status.full_text)
                        text = text.replace("\n", " ")
                        text = text.replace("\n", " ")
                        text = text.replace("\n", " ")
                        text = text.replace("\r", " ")
                        text = text.replace("\r", " ")
                        text = text.replace("\\", "\\\\")
                        text = text.replace("\"", "\\\"")
                        text = text.replace("\\''", "\\\\\'")
                        # date = date.split(" ")[0] 날짜만 받기
                        print("{\"date\": \"%s\", \"text\":\"%s\", \"long\":\"%s\", \"lat\":\"%s\", \"place\":\"%s\"}," % (date, text, XY[0], XY[1], place))
                        #print("{\"date\": \"%s\", \"text\":\"%s\"}," % (date, text))

                    elif '2017' in date:
                        break
                print("]},")
            except:
                print("]},")
                continue


        print("]}")