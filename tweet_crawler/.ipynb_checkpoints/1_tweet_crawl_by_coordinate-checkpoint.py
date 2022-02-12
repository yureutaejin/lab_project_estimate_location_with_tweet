import tweepy
import sys

# input key information from tweet application
from tweepy import StreamListener
from tweepy import Stream

consumer_key="XjQhR4ufXrbarK8DhIfkhsUMV"
consumer_secret="IUZc240ib8KaV9sOijV7I20lo2DZGJGWBzbE3oK6AIctFLQMWo"
access_token="1455834250054287362-jbQV7EVpNWBJtP4pmRWTZida2CTW2N"
access_token_secret="RHTaZGLpcbbwdv4U9y9FZ3oF5MijBjaeR9GJAbBZ4Arcy"

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

    # 좌표값 입력 list
    boundary_list = []
    while (len(boundary_list) != 4):
        input_boundary = float(input("input coordinate of boundary {}\n".format(len(boundary_list)+1)))
        boundary_list.append(input_boundary)
    print("boundary_list = {}".format(boundary_list))

    print("start")
   # open txt file to save the data

    stream = Stream(auth, l)

    with open('1_result_data/boston.txt', 'a' , encoding='utf-8') as tf:
        sys.stdout = tf
        print("{")
        #print("%s"%Users.location)
        #stream.filter(follow=[Users.location])

        while True:
             try:
                 # Call tweepy's userstream method
                 # Use either locations or track, not both
                 stream.filter(locations=boundary_list)  ##bounding box around USA->coordinate box
                 break
             except:
                 # Abnormal exit: Reconnect
                 print("}")
                 tf.close()

# boston: -71.110978, 42.277638, -71.056103, 42.337731
if __name__ == '__main__':
    main()