# 콤마 다음 "]}," 으로 되어있는 곳 번호 저장하고 인덱스 찾아서 지우기

import json
import sys
import tweepy

third_result_data_name_list = ['Fort Worth']

for city_name in third_result_data_name_list:

    with open('/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/tweet_data/3_result_data/{}_user_timeline_with_coord7.json'.format(city_name), 'r', encoding="utf-8-sig") as tw_file:

        list_of_lines = tw_file.readlines()

    with open('/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/tweet_data/3_result_data/{}_user_timeline_with_coord7.json'.format(city_name),'r', encoding="utf-8-sig") as tw_file:
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
                print(old_str)
                print(list_of_lines[line_num-1])
                print()
            line_num += 1

    print(str(line_index) + '\n')


    with open('/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/tweet_data/4_result_data/{}_user_timeline_with_coord7.json'.format(city_name), 'w') as tw_file:
        tw_file.writelines(list_of_lines)

