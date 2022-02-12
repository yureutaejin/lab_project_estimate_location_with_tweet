from bs4 import BeautifulSoup as bs
from selenium import webdriver
import sys

import json

input_location = input("please input location you want\n")
# 뉴스 크롤러
locations = [input_location]
driver = webdriver.Chrome('/Users/jinyuntae/Desktop/development_tool/chromedriver')

with open('/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/news_data/1_result_data/1_2018_CNNtest_{}.json'.format(input_location),'a',encoding='utf-8') as tf:
    sys.stdout = tf
    print("{\"Location\":[")
    # 10000개이상 검색이 안됨.
    for loc in locations:
        driver.get('https://edition.cnn.com/search/?size=10&q=' +loc+ '&from=' + str(4400) + '&page=' + str(441))
        soup = bs(driver.page_source, 'html.parser')
        rangenum = soup.find("div", {"class": "cnn-search__results-count"}).text
        crawlrange = int(rangenum.split(" ")[5])

        crawlrange = int(crawlrange / 10) + 1
        print("{\"%s\":["%(loc))
        #문제점 --> 10000개 이상 못넘감...........

        for i in range(441,crawlrange):
            pagenum = str(i)

            URL = 'https://edition.cnn.com/search/?size=10&q='+loc+'&from='+str((i-1)*10)+'&page=' + str(i)
            driver.get(URL)

            soup = bs(driver.page_source, 'html.parser')
            result = soup.find_all("div", {"class": "cnn-search__result-contents"})


            for i in range(len(result)):
                newslink = str(result[i].find("a")["href"])
                subject = str(result[i].find("h3",{"class":"cnn-search__result-headline"}).text)
                timestamp = str(result[i].find("div",{"class":"cnn-search__result-publish-date"}).text)
                result_body = str(result[i].find("div",{"class":"cnn-search__result-body"}).text)
                newslink = newslink.replace("//","")
                timestamp = timestamp.replace("\n","")
                subject = subject.replace("\n","")
                result_body = result_body.replace("\n                            ","")
                result_body = result_body.replace("\n                        ","")
                result_body = result_body.replace("\n "," ")
                result_body = result_body.replace("\n", " ")
                result_body = result_body.replace("\n", " ")
                result_body = result_body.replace("\n", " ")
                result_body = result_body.replace("\"", "\\\"")
                result_body = result_body.replace("\'", "\\\\\'")
                subject = subject.replace("\'","\\\\\'")
                subject = subject.replace("\"", "\\\"")


                #data = {"Location": relocation, "Title": headline, "Date": date, "text": text, "Link": page_link}
                print("{\"Title\":\"%s\",\"Date\":\"%s\",\"text\":\"%s\",\"Link\":\"%s\"}"%(subject,timestamp,result_body,newslink)+",")

        #print(result)
        print("]},")


    print("]}")