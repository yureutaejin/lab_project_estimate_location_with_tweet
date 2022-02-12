import json
import sys

# TODO 1: 각 사용자별로 트윗 개수 세기, 위치 정보가 있는 트윗 세기, 그 중 BOSTON 세기
# TODO 2: 위치 정보가 없는 사람들은 BOSTON 이라고 볼 수 있는가? 아닌가? 구분할 방법은?

# 한방에 돌릴때 사용
# third_result_data_name_list = ['boston', 'denver', 'el_paso', 'detroit', 'jackonville_florida', 'las_vegas', 'memphis', 'nashville', 'seattle', 'washington_DC']

# third_result_data_name_list = ['Boston', 'Detroit', 'Jacksonville', 'San Francisco', 'Fort Worth']
fourth_result_data_name_list = ['Fort Worth']

for city_name in fourth_result_data_name_list:
    with open('/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/tweet_data/4_result_data/{}_user_timeline_with_coord7.json'.format(city_name), encoding="UTF-8") as twfile_geo:
        twfile_geo = twfile_geo.read()
        tw_geo_data = json.loads(twfile_geo)
        total_usernum = len(tw_geo_data['users'])


    with open('/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/tweet_data/5_result_data/{}_user_filtered_count0.json'.format(city_name), 'w', encoding="UTF-8") as result:
        sys.stdout = result

        print("{\"users\":[")
        for i in range(total_usernum):
            user = tw_geo_data['users'][i]
            user_name = tw_geo_data['users'][i]['id']
            user_timeline = tw_geo_data['users'][i]['timeline']
            twnum = len(tw_geo_data['users'][i]['timeline'])
            month = []

            # heavy tweet user filter
            if len(user['timeline']) >= 200:
                # print("##")
                for j in range(twnum):
                    month.append(user_timeline[j]['date'].split("-")[1])
                wholemon = list(dict.fromkeys(month))
                if (len(wholemon) > 11):

                    #print("{\"id\":\"" + user_name + "\"," + "\"timeline\":[")

                    count = 0
                    for j in range(twnum):
                            if(city_name in user_timeline[j]['place']):
                                count += 1

                    if(count>0):
                        print("{\"id\":\"" + user_name + "\"," + "\"timeline\":[")
                        for tweet in tw_geo_data['users'][i]['timeline']:
                            date = tweet['date']
                            text = tweet['text']
                            place = tweet['place']
                            text = text.replace("\n", " ")
                            text = text.replace("\n", " ")
                            text = text.replace("\r", " ")
                            text = text.replace("\r", " ")
                            text = text.replace("\\", "\\\\")
                            text = text.replace("\"", "\\\"")
                            text = text.replace("\\''", "\\\\\'")

                            print("{\"date\": \"%s\", \"text\":\"%s\",\"place\":\"%s\"}," % (date, text, place))
                    else:
                        continue

                    print("]},")

            else:
                continue

        print("]}")

for city_name in fourth_result_data_name_list:

    with open('/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/tweet_data/5_result_data/{}_user_filtered_count0.json'.format(city_name), 'r', encoding="utf-8-sig") as tw_file:

        list_of_lines = tw_file.readlines()

    with open('/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/tweet_data/5_result_data/{}_user_filtered_count0.json'.format(city_name),'r', encoding="utf-8-sig") as tw_file:
        id_start = False
        comma_check = False
        text_ok = False

        line_num = 0
        line_index = []

        for line in tw_file:

            if "\"text\":" in line:
                text_ok = True
                if "},\n" in line:
                    comma_check = True
                else:
                    comma_check = False

            elif "\"id\":" in line:
                id_start = True

            elif (id_start == True) and (line == "]},\n") and (text_ok == True) and (comma_check == True):
                line_index.append(line_num)
                id_start = False
                text_ok = False
                old_str = list_of_lines[line_num-1]
                list_of_lines[line_num-1] = old_str[0:-2] + "\n"
            line_num += 1


    with open('/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/tweet_data/5_result_data/{}_user_filtered_count0.json'.format(city_name), 'w') as tw_file:
        tw_file.writelines(list_of_lines)