import json
import sys

def changedate(date):
    year = date.split(" ")[2]
    day = date.split(" ")[1]
    day = day.split(",")[0]
    month = date.split(" ")[0]

    if len(day)==1:
        day = "0"+str(day)

    if month=="Dec":
        month = "12"
    elif month=="Nov":
        month = "11"
    elif month=="Oct":
        month = "10"
    elif month=="Sep":
        month = "09"
    elif month=="Aug":
        month = "08"
    elif month=="Jul":
        month = "07"
    elif month=="Jun":
        month = "06"
    elif month=="May":
        month = "05"
    elif month=="Apr":
        month = "04"
    elif month=="Mar":
        month = "03"
    elif month=="Feb":
        month = "02"
    elif month=="Jan":
        month = "01"

    return str(year)+"-"+str(month)+"-"+str(day)

city_name = input("city name? ")

with open('/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/news_data/1_result_data/1_2018_CNNtest_{}.json'.format(city_name), encoding='UTF-8') as newsfile:
    newsfile = newsfile.read()
    newsdata = json.loads(newsfile, strict=False)

    tempt = (((newsdata['Location'])[0])[city_name])
    newsnum = len(tempt)



with open('/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/news_data/2_result_data/2_2018_CNNtest_{}.json'.format(city_name), 'w' ,encoding='UTF-8') as newsfile18:
    sys.stdout = newsfile18
    print("{\"news\":[")

    for i in range(newsnum):
        tempt = (((newsdata['Location'])[0])[city_name])[i]
        date = str(tempt['Date'])

        if '2018' in date:
            subject = str(tempt["Title"])
            timestamp = changedate(date)
            result_body = str(tempt['text'])
            result_body = result_body.replace("\"", "\\\"")
            result_body = result_body.replace("\\\'", "\\\\\'")
            subject = subject.replace("\\\'", "\\\\\'")
            subject = subject.replace("\"", "\\\"")
            newslink = str(tempt["Link"])

            print("{\"Title\":\"%s\",\"Date\":\"%s\",\"text\":\"%s\",\"Link\":\"%s\"}" % (subject, timestamp, result_body, newslink) + ",")
        else:
            continue

    print(']}')