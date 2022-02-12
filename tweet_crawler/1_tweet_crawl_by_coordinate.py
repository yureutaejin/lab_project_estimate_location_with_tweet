import tweepy
import sys

# input key information from tweet application
from tweepy import StreamListener
from tweepy import Stream

# consumer_key = "kzE47O3eNyiCUA18XdAVeEzWI"
# consumer_secret = "XDeTfxZJ5eaKHuIb4XV8YY82kSDSR1iuwx53h5Ak330T0Nk1Rb"
# access_token = "1013719331530608640-PhEIEKtu2NhvyFV2EXmGJqJk8Sx37f"
# access_token_secret = "7ggAhn1DHyAsDJxGpB1Uvo5wXV7zBmmSV9zuSOdGbpuFc"

consumer_key="T4OmeH7ZrH2jB8tPBMwuitlzv"
consumer_secret="NnlVSq6eGLAZM0HcptsmsEXJ22wrbCkhkOYLZ32EcSniyHXRv7"
access_token="1455834250054287362-pVWjp2r5TAJdcNT2K9GPtLsSujeAD3"
access_token_secret="Lg1WOe8CJT7qb5UmTz5PVPY1Yfm5J041lokEVBFAQ5BBU"

# create handler and request personal information
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# request access
auth.set_access_token(access_token, access_token_secret)
# create twitter API
api=tweepy.API(auth)

Users = dict()

class StdOutListener(StreamListener):
    def on_status(self, status):
        #print("Tweet Text: ", status.text)
        try:
            Users = status.user
            #
            # print("%s"%Users)
            infos = [Users.id, Users.screen_name, Users.location]
        except:
            pass
        print(("\"user\": { \"id\": %s, \"screen_name\": \"%s\", \"location\": \"%s\"}" % (infos[0], infos[1], infos[2])+","))

def main():
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # # 도시 좌표 파일 추출
    # with open('coordinates_test.txt', 'r', encoding='utf-8') as coordinate_txt:
    #
    #     city_list = []
    #     temp_txt = []
    #
    #     for line in coordinate_txt:
    #
    #         if (line != "") and (len(temp_txt) != 3):
    #             temp_txt.append(line.strip())
    #
    #         else:
    #             city_list.append(temp_txt)
    #             temp_txt = []
    #             continue

    city_name = input("city name? ")
    print("start")
   # open txt file to save the data

    # for i in city_list:
    #     city_name = i[0]
    #     order_location = i[1]

    with open('/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/tweet_data/1_result_data/{}.json'.format(city_name), 'a', encoding='utf-8') as tf:
        sys.stdout = tf
        print("{")
        stream = Stream(auth, l)
        #print("%s"%Users.location)
        #stream.filter(follow=[Users.location])

        while True:
             try:
                 # Call tweepy's userstream method
                 # Use either locations or track, not both
                 #stream.filter(locations=boundary_list)  ##bounding box around USA->coordinate box
                 # exec(order_location)
                 stream.filter(locations= [-71.110978, 42.277638, -71.056103, 42.337731])
                 break
             except:
                 # Abnormal exit: Reconnect
                 print("}")
                 tf.close()

# Boston: -71.110978, 42.277638, -71.056103, 42.337731
# SanFrancisco: -122.532067, 37.713074, -122.351590, 37.821454
# Indianapolis: -86.339166, 39.644215, -85.931594, 40.077050
# Jacksonville: -82.081064, 30.121330, -81.309562, 30.557877
# Denver: -105.098014, 39.633718, -104.625815, 39.907805
if __name__ == '__main__':
    main()